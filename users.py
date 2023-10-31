from flask import Flask, render_template, redirect, request, session, jsonify
from flask_session import Session
from pymysql import connect
from pymysql.cursors import re, DictCursor
import hashlib

app = Flask(__name__)
# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'skanin is the best'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
session = Session(app)
print(session)

# Connect to the database
connection = connect(host='localhost',
                             user='root',
                            #  password='passwd',
                             database='skanin_db',
                             charset='utf8mb4',
                             cursorclass=DictCursor)

app.route('/', methods=['GET'])
def index():
    return jsonify({'status': None})

@app.route('/login', methods=['GET'])
def login():
    # Message if succesfully logged in
    msg = 'succcess'
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        
        # Check if account exists using MySQL
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
            # Fetch one record and return the result
            account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['username'] = account['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect user credentials'
    return jsonify({'msg':msg, username:session})


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

## Main
if __name__ == '__main__':
    app.run(host='localhost',port=8080)