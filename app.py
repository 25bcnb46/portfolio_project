from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app) # This allows your frontend to talk to your backend safely

def init_db():
    conn = sqlite3.connect('portfolio.db') 
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db() 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    try:
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        query = "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)"
        cursor.execute(query, (name, email, message))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"status": "success", "message": "Message saved successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/messages')
def view_messages():
    try:
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        conn.close()

        # Build a simple HTML list to display the data
        output = "<h1>Live Database Messages</h1><ul style='font-family: Arial; line-height: 1.8;'>"
        for row in rows:
            output += f"<li><strong>Name:</strong> {row[1]} | <strong>Email:</strong> {row[2]} | <strong>Message:</strong> {row[3]}</li>"
        output += "</ul><br><a href='/'>Go back to Portfolio</a>"
        
        return output
    except Exception as e:
        return f"Database error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
