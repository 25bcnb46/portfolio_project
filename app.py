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

if __name__ == '__main__':
    app.run(debug=True)