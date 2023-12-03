from flask import Flask, render_template, redirect, request, jsonify, session, Blueprint
# from flask_session import Session
from pymysql import connect
from pymysql.cursors import re, DictCursor
import hashlib
import dotenv
import os
import re
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

# Load the environment variables
dotenv.load_dotenv()

users_bp = Blueprint('users',__name__)
# Change this to your secret key (it can be anything, it's for extra protection)
users_bp.secret_key = os.getenv("SECRET_KEY")
# users_bp.config["SESSION_PERMANENT"] = False
# users_bp.config["SESSION_TYPE"] = "filesystem"
# session = Session(users_bp)
# print(session)

# Connect to the database
connection = connect(host=os.getenv("DATABASE_URL"),
                    user=os.getenv("USER"),
                    password=os.getenv("PASSWORD"),
                    database=os.getenv("DATABASE_NAME"),
                    cursorclass=DictCursor,
                    # port=int(os.getenv("DATABASE_PORT"))
                    )


@users_bp.route('/signup', methods=['POST'])
def signup():
    # signup route checking that all fields are filled
    # will add method to continue signup even lesser priority fields are empty
    msg = ''
    DATA = request.get_json()
    # Check if form fields POST requests exist (user submitted form)
    if (request.method == 'POST' and 'username' in DATA 
        and 'password' in DATA and 'email' in DATA 
        # and 'first_name' in DATA and 'last_name' in DATA
        # and 'contact' in DATA
        ):
        if session.get("loggedin") == True:
            return jsonify({'msg':"You are already logged in"}),400
        # Create variables for easy access
        username = DATA['username']
        password = DATA['password']
        email = DATA['email']
        if 'first_name' in DATA:
            if DATA['first_name'] != '': first_name = DATA['first_name']
        else: first_name=None
        if 'last_name' in DATA:
            if DATA['last_name'] != '': last_name = DATA['last_name']
        else: last_name=None
        if 'contact' in DATA:
            if DATA['contact'] != '': contact = DATA['contact']
        else: contact=None
        flag = 0 ## checker if error occured
        
        ## Password Requirements:
        ## at least 8 length, one small letter, one big letter
        ## one number, one special character
        if len(password) < 8 : msg += "Password must be at least 8 characters. "; flag = 1
        if re.search('[a-z]', password) is None:msg += "Password must contain at least 1 small character. ";flag = 1
        if re.search('[A-Z]', password) is None:msg += "Password must contain at least 1 big character. ";flag = 1
        if re.search('[0-9]', password) is None:msg += "Password must contain at least 1 number. ";flag = 1
        if re.compile("[@_!#$%^&*()<>?/|}{~:]").search(password) is None: msg = "Password must contain at least one special character. ";flag = 1

        ## Username Checking
        if len(username) < 3: msg += "Username must be at least 3 characters. "; flag = 1
        
        ## Contact Checking
        if contact != None and len(contact) != 11: msg += "Contact must be 11 digits. "; flag = 1
        
        ## Email Checking
        if ("@" in email and "." in email.split("@")[1]) == False:
            msg += "Email must be a valid email address. "; flag = 1
            
        
        ## Check if error occured
        if flag == 1: 
            return jsonify({"msg":msg}), 400
        
        
        
        # Retrieve the hashed password
        hash = password + users_bp.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists using MySQL
        connection.ping(reconnect=True)
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
            return jsonify({'msg':msg}), 200
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
    return jsonify({'msg':msg}), 500

@users_bp.route('/login', methods=['POST'])
def login():
    # login route only using username and password for now
    # soon add email for login
    msg = 'Incorrect user credentials'
    DATA = request.get_json()
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'password' in DATA and ('email' in DATA or 
                                                                    'username' in DATA ):
        # Create variables for easy access
        if session.get("loggedin") == True:
            return jsonify({'msg':"You are already logged in"}),400
        try:
            value = DATA['username']
            key = 'username'
        except:
            value = DATA['email']
            key = 'email'
        password = DATA['password']
        # Retrieve the hashed password
        hash = password + users_bp.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        
        # Check if account exists using MySQL
        connection.ping(reconnect=True)
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
            return jsonify({'msg':msg, 'username':session.get('username'), 'user_id':session.get('user_id')}), 200
        else:
            # Account doesnt exist or username/password incorrect
            return jsonify({'msg':msg}), 400
    return jsonify({'msg':msg}), 400
        

@users_bp.route('/update_user', methods = ['GET', 'PUT'])
def update_user():
    if session.get("loggedin") == False:
        return jsonify({'msg':"You are not logged in"}),400
    DATA = request.get_json()
    # user update with auto fill in initial GET request
    user_id = session.get('user_id')
    username = session.get('username')
    email = session.get('email')
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    contact = session.get('contact')
    if request.method == 'GET':
        msg = 'Autofill information'
        return jsonify({'msg':msg,
                        'username':username, 
                        'user_id':user_id, 
                        'email':email,
                        'first_name':first_name,
                        'last_name':last_name,
                        'contact':contact,
                        }), 200
    # Check if form fields POST requests exist (user submitted form)
    elif (request.method == 'PUT' and 'password' in DATA):
        # Create variables for easy access
        password = DATA['password']
        if "username" in DATA and DATA['username'] != '': new_username = DATA['username']
        else: new_username = username
        if "email" in DATA and DATA['email'] != '': new_email = DATA['email']
        else: new_email = email
        if "first_name" in DATA and DATA['first_name'] != '': new_first_name = DATA['first_name']
        else: new_first_name = first_name
        if "last_name" in DATA and DATA['last_name'] != '': new_last_name = DATA['last_name']
        else: new_last_name = new_last_name
        if "contact" in DATA and DATA['contact'] != '': new_contact = DATA['contact']
        else: new_contact = contact
        if "new_password" in DATA and DATA['new_password'] != '': 
            new_password = DATA['new_password']
        else: new_password = password
        
        flag = 0 ## checker if error occured
        
        ## Password Requirements:
        ## at least 8 length, one small letter, one big letter
        ## one number, one special character
        if len(new_password) < 8 : msg += "Password must be at least 8 characters. "; flag = 1
        if re.search('[a-z]', new_password) is None:msg += "Password must contain at least 1 small character. ";flag = 1
        if re.search('[A-Z]', new_password) is None:msg += "Password must contain at least 1 big character. ";flag = 1
        if re.search('[0-9]', new_password) is None:msg += "Password must contain at least 1 number. ";flag = 1
        if re.compile('[@_!#$%^&*()<>?/\|}{~:]').search(new_password) is None: msg = "Password must contain at least one special character. ";flag = 1

        ## Username Checking
        if len(username) < 3: msg += "Username must be at least 3 characters. "; flag = 1
        
        ## Contact Checking
        if contact != None and len(contact) != 11: msg += "Contact must be 11 digits. "; flag = 1
        
        ## Email Checking
        if ("@" in email and "." in email.split("@")[1]) == False:
            msg += "Email must be a valid email address. "; flag = 1
            
        
        ## Check if error occured
        if flag == 1: 
            return jsonify({"msg":msg}), 400
        
        # Hash old and new password
        hash = password + users_bp.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        
        hash = new_password + users_bp.secret_key
        hash = hashlib.sha1(hash.encode())
        new_password = hash.hexdigest()
        # Check if account exists using MySQL
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE user_id != '{user_id}' AND (username = '{username}' OR email = '{email}')") #cursor.execute(f"SELECT * FROM users WHERE user_id = '{session.get('user_id')}'")
            # Fetch one record return the result
            account = cursor.fetchone() 
        connection.commit()
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
                    return jsonify({'msg':msg}), 400
                
            with connection.cursor() as cursor:
                cursor = connection.cursor()
                cursor.execute(f'''UPDATE `users` SET `username`='{new_username}', `email`='{new_email}',
                               `first_name`='{new_first_name}', `last_name`='{new_last_name}',
                               `contact`='{new_contact}', `password`='{new_password}' 
                               WHERE `user_id` = '{user_id}'
                               ''')
            connection.commit()
            session['username'] = new_username
            session['first_name'] = new_first_name
            session['last_name'] = new_last_name
            session['contact'] = new_contact
            session['email'] = new_email
            msg = 'Account updated'
        elif account['email']==email and email != new_email:
            # Message if email is taken
            msg = 'Email already taken'
        elif account['username']==username and username != new_username:
            # Message if username is taken
            msg = 'Username already taken'
        elif account['contact']==contact and contact != new_contact:
            # Message if contact is taken
            msg = 'Contact already taken'
        else:
            msg = 'Unknown error. Contact website administrator'
    elif 'password' not in DATA:
        msg = 'Please enter your current password corrently'

    return jsonify({'msg':msg}), 400

@users_bp.route("/logout", methods=['POST'])
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
            return jsonify({'msg':msg}), 200
    msg = "error logging out"
    return jsonify({'msg':msg}), 500

@users_bp.route("/get_user", methods=["GET"])
def get_user():
    msg = ''
    # return user credentials from session
    if request.method == 'GET':
        msg = 'Current user retrieved'
        return jsonify({'msg':msg,'username':session.get('username'), 'user_id':session.get('user_id'),
                        'loggedin':session.get('loggedin'), 'email':session.get('email'),
                        'first_name':session.get('first_name'), 'last_name':session.get('last_name')
                        }), 200
    return jsonify({'msg':msg}), 400

@users_bp.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 400

    access_token = create_access_token(identity=email)
    response = {"access_token":access_token}
    return response, 200
## ADD forget_password FUNCTION AND ROUTE
##
##
##

## Main
# if __name__ == '__main__':
#     users_bp.run(host='localhost',port=8080, debug=True)