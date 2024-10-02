import mysql.connector

# Replace these values with your MySQL server credentials
config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',  # Or the IP address of your MySQL server
    'database': 'ryadb'
}

try:
    # Establish a connection
    connection = mysql.connector.connect(**config)
    print("Connection successful!")

    # Create a cursor object using the connection
    cursor = connection.cursor()

    # Execute a simple query
    cursor.execute("SELECT DATABASE();")
    result = cursor.fetchone()
    print("Connected to database:", result[0])

    cursor.execute("SELECT * FROM Books")

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Print the rows
    for row in rows:
        print(row)
except mysql.connector.Error as err:
    print("Error:", err)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
