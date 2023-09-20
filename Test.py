@app.route('/update', methods=['POST'])
def update_database():
    try:
        excel_file = request.files['excel_file']

        if excel_file:
            # Read the Excel data into a Pandas DataFrame
            df = pd.read_excel(excel_file)

            # Iterate through the DataFrame and update the database
            for _, row in df.iterrows():
                client = Client(
                    client_prefix=row['client_prefix'],
                    client_name=row['client_name'],
                    client_legal_name=row['client_legal_name'],
                    client_website=row['client_website'],
                    client_digital_catalog=row['client_digital_catalog'],
                )
                db.session.add(client)
            db.session.commit()

            return jsonify({"message": "Data updated successfully"})
        else:
            return jsonify({"message": "No Excel file provided"})
    except Exception as e:
        return jsonify({"error": str(e)})
