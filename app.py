from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse
import pymysql
import os

app = Flask(__name__)
CORS(app) 

# --- 1. Cloud Database Connection Setup ---
def get_db_connection():
    # This securely grabs your database link from Render's settings
    db_url = os.getenv("DATABASE_URL") 
    
    if not db_url:
        raise Exception("DATABASE_URL is missing! Please add it to Render.")

    # This breaks the URL into username, password, host, etc.
    parsed = urlparse(db_url)
    
    conn = pymysql.connect(
        host=parsed.hostname,
        port=parsed.port,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path[1:], # Removes the '/' from the database name
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

# --- 2. Create the Table (If it doesn't exist) ---
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # MySQL uses AUTO_INCREMENT instead of SQLite's AUTOINCREMENT
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Database setup skipped or failed:", e)

# --- 3. Main Portfolio Page ---
@app.route('/')
def home():
    return render_template('index.html')

# --- 4. Route to Catch Form Submissions ---
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # MySQL uses %s instead of ? to securely insert data
        query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, message))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"status": "success", "message": "Saved permanently to the Cloud!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# --- 5. Secret Route to View the Database ---
@app.route('/messages')
def view_messages():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        conn.close()

        output = "<h1>Live Cloud Database Messages</h1><ul style='font-family: Arial;'>"
        for row in rows:
            # We use row['name'] because DictCursor makes it easy to read
            output += f"<li><strong>Name:</strong> {row['name']} | <strong>Email:</strong> {row['email']} | <strong>Message:</strong> {row['message']}</li>"
        output += "</ul><br><a href='/'>Go back to Portfolio</a>"
        
        return output
    except Exception as e:
        return f"Database error: {str(e)}"

if __name__ == '__main__':
    # Initialize DB only if URL is present (prevents local crashes)
    if os.getenv("DATABASE_URL"):
        init_db()
    app.run(debug=True)
