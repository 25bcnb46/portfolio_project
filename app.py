from flask import Flask, render_template, request, jsonify
import sqlite3 # Built-in Python library! No pip install needed.

app = Flask(__name__)

# --- NEW: This automatically creates your database and table! ---
def init_db():
    # This creates a file called 'portfolio.db' in your folder
    conn = sqlite3.connect('portfolio.db') 
    cursor = conn.cursor()
    # Create the table if it doesn't exist yet
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

# Run the setup function when the app starts
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
        # Connect to the SQLite database file
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        
        # Insert the data (SQLite uses ? instead of %s)
        query = "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)"
        cursor.execute(query, (name, email, message))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"status": "success", "message": "Message saved to SQLite database!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)