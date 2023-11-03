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

@app.route('/signup', methods=['POST'])
def signup():
    msg = ''
    # Check if form fields POST requests exist (user submitted form)
    if (request.method == 'POST' and 'username' in request.form and 'password' in request.form 
        and 'email' in request.form and 'first_name' in request.form and 'last_name' in request.form
        and 'contact' in request.form):
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact = request.form['contact']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists using MySQL
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' OR email = '{email}' OR contact = '{contact}'")
            # Fetch one record return the result
            account = cursor.fetchone() 
            print(account)
        if account == None:
            # Account doesnt exist. New account verified
            with connection.cursor() as cursor:
                cursor = connection.cursor()
                cursor.execute(f'''INSERT INTO `users`(`username`, `password`, `email`,`first_name`,`last_name`,`contact`) 
                                VALUES ('{username}','{password}','{email}','{first_name}','{last_name}','{contact}')''')
            connection.commit()
            msg = 'Account created succesfully'
        elif account['email']==email:
            # Message if email is taken
            msg = 'Email already taken'
        elif account['username']==username:
            # Message if username is taken
            msg = 'Username already taken'
        elif account['contact']==contact:
            # Message if username is taken
            msg = 'Contact number already taken'
        else:
            msg = 'Unknown error. Contact website administrator'
    return jsonify({'msg':msg})

@app.route('/login', methods=['POST'])
def login():
    msg = 'Error login'
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
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'; ")
            # Fetch one record return the result
            account = cursor.fetchone() 
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['username'] = account['username']
            session['first_name'] = account['first_name']
            session['last_name'] = account['last_name']
            session['contact'] = account['contact']
            session['email'] = account['email']
            # Redirect to home page
            msg =  'Logged in successfully!'
            return jsonify({'msg':msg, 'username':session.get('username'), 'user_id':session.get('user_id')})
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect user credentials'
            return jsonify({'msg':msg})
    return jsonify({'msg':msg})
        

@app.route('/update_user', methods = ['GET', 'POST'])
def update_user():
    user_id = session.get('user_id')
    username = session.get('username')
    email = session.get('email')
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    contact = session.get('contact')
    if request.method == 'GET':
        return jsonify({'username':username, 
                        'user_id':user_id, 
                        'email':email,
                        'first_name':first_name,
                        'last_name':last_name,
                        'contact':contact,
                        })
    # Check if form fields POST requests exist (user submitted form)
    elif (request.method == 'POST' and 'password' in request.form):
        # Create variables for easy access
        if request.form['username'] != '': username = request.form['username']
        if request.form['email'] != '': email = request.form['email']
        if request.form['first_name'] != '': first_name = request.form['first_name']
        if request.form['last_name'] != '': last_name = request.form['last_name']
        if request.form['contact'] != '': contact = request.form['contact']

        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists using MySQL
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE user_id != '{user_id}' AND (username = '{username}' OR email = '{email}' OR contact = '{contact}')") #cursor.execute(f"SELECT * FROM users WHERE user_id = '{session.get('user_id')}'")
            # Fetch one record return the result
            account = cursor.fetchone() 
        if account == None:
            # Account doesnt exist. Update account verified
            with connection.cursor() as cursor:
                cursor = connection.cursor()
                cursor.execute(f'''SELECT * from `users` WHERE `user_id` = '{user_id}'
                               ''')
                account = cursor.fetchone() 
                if account['password'] != password:
                    # Incorrect Password
                    msg = 'Incorrect old password'
                    return jsonify({'msg':msg})
                
            if request.form['new_password'] != '': 
                new_password = request.form['new_password']
                hash = new_password + app.secret_key
                hash = hashlib.sha1(hash.encode())
                new_password = hash.hexdigest()
            else: new_password = password
            with connection.cursor() as cursor:
                cursor = connection.cursor()
                cursor.execute(f'''UPDATE `users` SET `username`='{username}', `email`='{email}',
                               `first_name`='{first_name}', `last_name`='{last_name}',
                               `contact`='{contact}', `password`='{new_password}' 
                               WHERE `user_id` = '{user_id}'
                               ''')
            connection.commit()
            msg = 'Account updated'
        elif account['email']==email:
            # Message if email is taken
            msg = 'Email already taken'
        elif account['username']==username:
            # Message if username is taken
            msg = 'Username already taken'
        elif account['contact']==contact:
            # Message if username is taken
            msg = 'Contact already taken'
        else:
            msg = 'Unknown error. Contact website administrator'
    elif 'password' not in request.form:
        msg = 'Please enter your current password corrently'

    return jsonify({'msg':msg})

@app.route("/logout", methods=['GET'])
def logout():
    msg = 'User Logged Out'
    session.pop("username", None)
    session.pop("user_id", None)
    session.pop("loggedin", False)
    return jsonify({'msg':msg})

@app.route("/get_user", methods=["GET"])
def get_user():
    return jsonify({'username':session.get('username'), 'user_id':session.get('user_id'),'loggedin':session.get('loggedin')})

## Main
if __name__ == '__main__':
    app.run(host='localhost',port=8080)