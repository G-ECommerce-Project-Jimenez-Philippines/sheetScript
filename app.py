from flask import Flask, request, jsonify
import mysql.connector
from googleapiclient.discovery import build
from google.oauth2 import service_account

app = Flask(__name__)

# Function to establish a database connection
def get_db_connection():
    # Replace these with your MySQL database connection details
    config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "db_grow_ecommerce",
    }
    connection = mysql.connector.connect(**config)
    return connection

# Replace with the path to your client_id.json file
SERVICE_ACCOUNT_FILE = 'C:/xampp/htdocs/test/majestic-casing-399506-63483a50df5f.json'
SPREADSHEET_ID = '16t1ywRGyUbMBmgI1J082cOr_-LRv10ljVBSPgNMjWW4'
SHEET_NAME = 'Test'  # Replace with your actual sheet name

def get_google_sheets_service():
    creds = None
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    return service

@app.route('/api/invoices', methods=['GET'])
def get_invoices():
    try:
        # Get pagination parameters from the request (default to page 1 and limit 10)
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 18000))

        # Calculate the start and end indices for the current page
        start_index = (page - 1) * limit

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Execute an SQL query to fetch invoice data
        cursor.execute('SELECT * FROM import_chub_remit LIMIT %s OFFSET %s', (limit, start_index))

        # Fetch the records for the current page
        records = cursor.fetchall()

        # Close the database connection
        connection.close()

        # Create a list of lists containing your invoice data
        data_to_insert = [[record["Balance Due"], record["Action Code Description"], record["Balance Due Currency"], record["Batch Date"], record["Batch Number"], record["Check Number"], record["Discount"], record["Discount Currency"], record["EFT Number"], record["Format Code"], record["Handling Code"], record["Insert Date"], record["Invoice Adjustment Date"], record["Invoice Adjustment Description"], record["Invoice Adjustment Number"], record["Invoice Adjustment Reason"], record["Invoice Amount"], record["Invoice Amount Currency"], record["Invoice Date"], record["Invoice Discount"], record["Invoice Discount Currency"], record["Invoice Number"], record["Invoice To Customer Number"], record["Line Balance Due"], record["Line Balance Due Currency"], record["Line Discount"], record["Line Discount Currency"], record["Merchant"], record["Payment Date"], record["Payment Due Date"], record["Payment Method"], record["PO Date"], record["PO Number"], record["Remit To Address 1"], record["Remit To Address 2"], record["Remit To Address 3"], record["Remit To City"], record["Remit To Customer Number"], record["Remit To Name 1"], record["Remit To Name 2"], record["Remit To Postal Code"], record["Remit To State"], record["Retailer Account Number"], record["Retailer EIN"], record["Retailer Routing Number"], record["RMA Number"], record["Supplier Account Number"], record["Supplier EIN"], record["Supplier Routing Number"], record["Transaction Line Number"]] for record in records]

        # Get the Google Sheets service
        sheets_service = get_google_sheets_service()

        # Update the Google Spreadsheet with the new data
        sheet_range = 'A1'  # Start from cell A1
        body = {
            'values': data_to_insert
        }

        result = sheets_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=sheet_range,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()

        return jsonify({"message": "Data added to Google Sheets."})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
