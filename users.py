from flask import Flask, render_template, redirect, request, jsonify, session
# from flask_session import Session
from pymysql import connect
from pymysql.cursors import re, DictCursor
import hashlib
import dotenv
import os
import re

# Load the environment variables
dotenv.load_dotenv()

app = Flask(__name__)
# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# session = Session(app)
# print(session)

# Connect to the database
connection = connect(host=os.getenv("DATABASE_URL"),
                    user=os.getenv("USER"),
                    # password=os.getenv("PASSWORD"),
                    database=os.getenv("DATABASE_NAME"),
                    cursorclass=DictCursor)

app.route('/', methods=['GET'])
def index():
    return jsonify({'status': None})

@app.route('/signup', methods=['POST'])
def signup():
    # signup route checking that all fields are filled
    # will add method to continue signup even lesser priority fields are empty
    msg = ''
    # Check if form fields POST requests exist (user submitted form)
    if (request.method == 'POST' and 'username' in request.form 
        and 'password' in request.form and 'email' in request.form 
        # and 'first_name' in request.form and 'last_name' in request.form
        # and 'contact' in request.form
        ):
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if 'first_name' in request.form:
            if request.form['first_name'] != '': first_name = request.form['first_name']
        else: first_name=None
        if 'last_name' in request.form:
            if request.form['last_name'] != '': last_name = request.form['last_name']
        else: last_name=None
        if 'contact' in request.form:
            if request.form['contact'] != '': contact = request.form['contact']
        else: contact=None
        flag = 0 ## checker if error occured
        
        ## Password Requirements:
        ## at least 8 length, one small letter, one big letter
        ## one number, one special character
        if len(password) < 8 : msg += "Password must be at least 8 characters."; flag = 1
        if re.search('[a-z]', password) is None:msg += "Password must contain at least 1 small character.";flag = 1
        if re.search('[A-Z]', password) is None:msg += "Password must contain at least 1 big character.";flag = 1
        if re.search('[0-9]', password) is None:msg += "Password must contain at least 1 number.";flag = 1
        if re.compile('[@_!#$%^&*()<>?/\|}{~:]').search(password) is None: msg = "Password must contain at least one special character";flag = 1

        ## Username Checking
        if len(username) < 3: msg += "Username must be at least 3 characters"; flag = 1
        
        ## Contact Checking
        if contact != None and len(contact) != 11: msg += "Contact must be 11 digits"; flag = 1
        ## Check if error occured
        if flag == 1: 
            return jsonify({"msg":msg})
        
        
        
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists using MySQL
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' OR email = '{email}'")
            # Fetch one record return the result
            account = cursor.fetchone()
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
            # Message if contact is taken
            msg = 'Contact number already taken'
        else:
            msg = 'Unknown error. Contact website administrator'
    return jsonify({'msg':msg})

@app.route('/login', methods=['POST'])
def login():
    # login route only using username and password for now
    # soon add email for login
    msg = 'Incorrect user credentials'
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'password' in request.form and ('email' in request.form or 
                                                                    'username' in request.form ):
        # Create variables for easy access
        try:
            value = request.form['username']
            key = 'username'
        except:
            value = request.form['email']
            key = 'email'
        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        
        # Check if account exists using MySQL
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE {key} = '{value}' AND password = '{password}'; ")
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
            return jsonify({'msg':msg})
    return jsonify({'msg':msg})
        

@app.route('/update_user', methods = ['GET', 'POST'])
def update_user():
    # user update with auto fill in initial GET request
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
            # Message if contact is taken
            msg = 'Contact already taken'
        else:
            msg = 'Unknown error. Contact website administrator'
    elif 'password' not in request.form:
        msg = 'Please enter your current password corrently'

    return jsonify({'msg':msg})

@app.route("/logout", methods=['POST'])
def logout():
    # logout route and release session
    msg = ''
    if request.method == 'POST':
        msg = 'No user logged in'
        if session.get('loggedin') == True:
            msg = 'User Logged Out'
            session.pop("username", None)
            session.pop("user_id", None)
            session.pop("first_name", None)
            session.pop("last_name", None)
            session.pop("contact", None)
            session.pop("email", None)
            session.pop("loggedin", False)
    return jsonify({'msg':msg})

@app.route("/get_user", methods=["GET"])
def get_user():
    msg = ''
    # return user credentials from session
    if request.method == 'GET':
        msg = 'Current user retrieved'
        return jsonify({'msg':msg,'username':session.get('username'), 'user_id':session.get('user_id'),
                        'loggedin':session.get('loggedin'), 'email':session.get('email'),
                        'first_name':session.get('first_name'), 'last_name':session.get('last_name')
                        })
    return jsonify({'msg':msg})

## Main
if __name__ == '__main__':
    app.run(host='localhost',port=8080)