from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# 1. Connect to your XAMPP Database
db_config = {
    'host': 'localhost',
    'user': 'root',      # Default XAMPP username is 'root'
    'password': '',      # Default XAMPP password is blank
    'database': 'portfolio_db'
}

# 2. Show the homepage when someone visits your site
@app.route('/')
def home():
    # Flask will look inside the 'templates' folder for this file
    return render_template('index.html') 

# 3. Receive form data and save it to the database
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    try:
        # Open the drawer, write the data in the spreadsheet, close the drawer
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, message))
        
        conn.commit() # This saves the changes
        cursor.close()
        conn.close()
        
        return jsonify({"status": "success", "message": "Message saved to database!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)