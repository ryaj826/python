from flask import Flask, request, jsonify
import mysql.connector

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace these values with your MySQL server credentials
config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',  # Or the IP address of your MySQL server
    'database': 'ryadb'
}

# def connection:
#     mysql.connector.connect(**config)

# Initialize the SQLite database
def init_db():
    # conn = sqlite3.connect('ryadb.db')
    # cursor = conn.cursor()
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS users (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         name TEXT NOT NULL,
    #         email TEXT NOT NULL UNIQUE
    #     )
    # ''')
    # conn.commit()
    # conn.close()

    # Establish a connection
    conn = mysql.connector.connect(**config)
    print("Connection successful!")

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # Execute a simple query
    cursor.execute("SELECT DATABASE();")
    result = cursor.fetchone()
    print("Connected to database:", result[0])

#     cursor.execute("SELECT * FROM Books")

#     # Fetch all rows from the executed query
#     rows = cursor.fetchall()

#     # Print the rows
#     for row in rows:
#         print(row)
# except mysql.connector.Error as err:
#     print("Error:", err)

# finally:
#     # Close the cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()



# Home route
@app.route('/')
def home():
    return "Simple CRUD API with Flask and SQLite"

# Create a new book (C)
@app.route('/books', methods=['POST'])
def create_book():
    jdata = request.get_data(as_text=True)
    print(f"Received data: {jdata}")  # Log raw incoming data

    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    price = data.get('price')

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, price) VALUES (%s, %s, %s)', (title, author, price))
    conn.commit()
    # id = cursor.lastrowid
    conn.close()

    return jsonify({'title': title, 'author': author, 'price': price}), 201
    # return jsonify({'id': id, 'title': title, 'author': author, 'price': price}), 201

# Read all books (R)
@app.route('/books', methods=['GET'])
def get_books():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT Id, Title, Author, Price FROM books')
    books = cursor.fetchall()
    conn.close()

    return jsonify(books)

# Read a single book by ID (R)
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = %s', (id,))
    book = cursor.fetchone()
    conn.close()

    if book:
        return jsonify(book)
    else:
        return jsonify({'error': 'Book not found'}), 404

# Update a book by ID (U)
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    Id= data.get('id')
    title = data.get('title')
    author = data.get('author')
    price = data.get('price')

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET title = %s, author = %s, price= %s WHERE id = %s', (title, author, price, id))
    conn.commit()
    conn.close()

    return jsonify({'id': id, 'title': title, 'author': author, 'price':price})

# Delete a book by ID (D)
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = %s', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
