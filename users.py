from flask import Flask, render_template, redirect, request, jsonify, session
# from flask_session import Session
from pymysql import connect
from pymysql.cursors import re, DictCursor
import hashlib

app = Flask(__name__)
# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'skanin is the best'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# session = Session(app)
# print(session)

# Connect to the database
connection = connect(host='localhost',
                             user='root',
                            #  password='passwd',
                             database='skanin_db',
                            #  charset='utf8mb4',
                             cursorclass=DictCursor)

app.route('/', methods=['GET'])
def index():
    return jsonify({'status': None})

@app.route('/login', methods=['POST'])
def login():
    # Message if succesfully logged in
    msg = ''
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
            print(username, password)
            print(type(username), type(password))
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'; ")
            # Fetch one record return the result
            account = cursor.fetchone() 
        # If account exists in accounts table in out database
            print(account)
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['username'] = account['username']
            # Redirect to home page
            msg =  'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect user credentials'
            # print(account['user_id'], 'now working')
    # print(session['user_id')
    return jsonify({'msg':msg, 'username':session.get('username'), 'user_id':session.get('user_id')})


@app.route("/logout", methods=['GET'])
def logout():
    msg = 'User Logged Out'
    session.pop("username", None)
    session.pop("user_id", None)
    session.pop("loggedin", False)
    return {'msg':msg}

@app.route("/get_user", methods=["GET"])
def get_user():
    return jsonify({'username':session.get('username'), 'user_id':session.get('user_id'),'loggedin':session.get('loggedin')})

## Main
if __name__ == '__main__':
    app.run(host='localhost',port=8080)