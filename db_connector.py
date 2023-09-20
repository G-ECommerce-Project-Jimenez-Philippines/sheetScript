import mysql.connector

# Create a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",      # Replace with your MySQL server's hostname or IP address
    user="admin",  # Replace with your MySQL username
    password="root",  # Replace with your MySQL password
    database="db_grow_ecommerce.sql"   # Replace with the name of your MySQL database
)

# Create a cursor
cursor = connection.cursor()

try:
    # Execute an SQL query
    cursor.execute('SELECT * FROM import_chub_remit')  # Replace 'your_mysql_table' with your actual table name

    # Fetch the data
    records = cursor.fetchall()

    # Process and work with the fetched data
    for record in records:
        print(record)

except mysql.connector.Error as e:
    print("MySQL error:", e)

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
