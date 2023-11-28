from flask import Flask, render_template, redirect, request, jsonify, session, send_file
from pymysql import connect
from pymysql.cursors import re, DictCursor
import numpy as np
import cv2
from PIL import Image
import io
import dotenv
import hashlib
import os
from tensorflow.keras.models import load_model
import tensorflow_hub as hub
from tensorflow.keras.preprocessing import image
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

# Load the environment variables
dotenv.load_dotenv()

app = Flask(__name__)
# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


# Connect to the database
connection = connect(host=os.getenv("DATABASE_URL"),
                    user=os.getenv("USER"),
                    password=os.getenv("PASSWORD"),
                    database=os.getenv("DATABASE_NAME"),
                    cursorclass=DictCursor,
                    # port=int(os.getenv("DATABASE_PORT"))
                    )

image_size = (224)
channels = 3

############### HISTORY API ###############
@app.route("/get_history", methods=["GET"])
def get_history():
    if (request.method == 'GET'):
        user_id = session.get('user_id')
        ## Retrieving data from the database
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `history` WHERE `user_id` = {user_id} LIMIT 6")
            data = cursor.fetchall()
        connection.commit()
        
        ## Formatting retrieved data
        history={}
        for i in range(0, len(data)):
            ## Assnigning to history dictionary/object
            history[str(i)]= {'history_id':data[i]['history_id'],'user_id':data[i]['user_id'],
                              'stress_id':data[i]['stress_id'],'date_transaction':data[i]['date_transaction'],
                              'image_name':data[i]['image_name']}

        msg = 'Successfully retrieved history'
        return jsonify({'msg': msg, 'history':history})
    msg = 'Invalid request'
    return jsonify({'msg':msg})

# Create a route to serve images
@app.route('/get_image/<int:image_num>', methods=['GET'])
def get_image(image_num):
    try:
        # Fetch image data from the database based on image_id
        user_id = session.get('user_id')
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor.execute("SELECT rice_image FROM history WHERE user_id = %s LIMIT 6", (user_id,))
            image_data = cursor.fetchall()[image_num]
        connection.commit()

        if image_data:
            # Convert image bytes to numpy array
            image = Image.frombytes("RGB", (224, 224), image_data['rice_image']) 

            # Convert the image to a response
            image_io = io.BytesIO()
            image.save(image_io, 'JPEG')
            image_io.seek(0)

            return send_file(image_io, mimetype='image/jpeg'), 200
        else:
            return 'Image not found', 404
    except Exception as e:
        return str(e)
    
############### END OF HISTORY API ###############







############### RECOMMENDATION API ###############

# Model initialization
# Define the function to handle the KerasLayer when loading the model
def load_model_with_hub(path):
    class KerasLayerWrapper(hub.KerasLayer):
        def __init__(self, handle, **kwargs):
            super().__init__(handle, **kwargs)

    custom_objects = {'KerasLayer': KerasLayerWrapper}

    return load_model(path, custom_objects=custom_objects)

# Load the model using the defined function
model = load_model_with_hub('model/model.h5')

def preprocessData(data, image_size = 384):
    ## Main Preprocessing function for input images 
    img = cv2.resize(data,(image_size,image_size))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array *= 1./255
    return img_array

@app.route('/skan', methods=["POST"])
def skan():
    if request.method == 'POST' and 'image' in request.files:
        ## Retrieving user_id
        user_id = session.get('user_id')
        print(user_id)
        ## Prediction route accepting images and outputs prediction of A.I.
        ## Read Image from input and convert to CV2
        image = request.files['image']
        image_name=image.filename
        ## Checking file name if jpg jpeg or png
        if image_name.split('.')[-1] not in ["jpeg", "png", "jpg"]:
            msg = "Invalid file type. Submit only .jpg, .png, or .jpeg files."
            return jsonify({"msg":msg})
        pil_image = Image.open(image.stream).convert('RGB').resize((300, 300))
        data = np.array(pil_image)
        

        ## Image for saving
        rice_image = data.tobytes()

        ## Model prediction
        data = preprocessData(data)
        result = np.argmax(model(data))+1
        print(result)
        # print("INSERT HERE")
        # result = '3'
            ## End of prediction

        ## Getting Recommendation using output from model
        stress_id = int(result)
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * from rice_stress WHERE `stress_id` = {stress_id}")
            stress = cursor.fetchone()
        stress_name = stress['stress_name']
        stress_type = stress['stress_type']
        stress_level = stress['stress_level']
        description = stress['description']
        description_src = stress['description_src']
        recommendation = stress['recommendation']
        recommendation_src = stress['recommendation_src']
        msg = 'Successfully retrieved recommendation'

        ## Creating history entry for transaction
        with connection.cursor() as cursor:
            # print("working")
            sql = "INSERT INTO `history` (`user_id`, `stress_id`, `rice_image`, `image_name`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user_id, stress_id, rice_image, image_name))
        connection.commit()
        
        return jsonify({'msg':msg, 'stress_name':stress_name, stress_type:'stress_type',
                        'stress_level':stress_level, 'description':description, 'description_src':description_src,
                        'recommendations':recommendation, 'recommendation_src':recommendation_src})
    msg = 'Invalid request'
    return jsonify({'msg':msg})

############### END OF RECOMMENDATION API ###############





############### USERS API ###############

jwt = JWTManager(app)

@app.route('/')
def index():
    return jsonify({'status': 200})

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
            return jsonify({"msg":msg})
        
        
        
        # Retrieve the hashed password
        hash = password + app.secret_key
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
            return jsonify({'msg':msg, 'username':session.get('username'), 'user_id':session.get('user_id')})
        else:
            # Account doesnt exist or username/password incorrect
            return jsonify({'msg':msg})
    return jsonify({'msg':msg})
        

@app.route('/update_user', methods = ['GET', 'PUT'])
def update_user():
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
                        })
    # Check if form fields POST requests exist (user submitted form)
    elif (request.method == 'PUT' and 'password' in request.form):
        # Create variables for easy access
        password = request.form['password']
        if "username" in request.form and request.form['username'] != '': new_username = request.form['username']
        else: new_username = username
        if "email" in request.form and request.form['email'] != '': new_email = request.form['email']
        else: new_email = email
        if "first_name" in request.form and request.form['first_name'] != '': new_first_name = request.form['first_name']
        else: new_first_name = first_name
        if "last_name" in request.form and request.form['last_name'] != '': new_last_name = request.form['last_name']
        else: new_last_name = new_last_name
        if "contact" in request.form and request.form['contact'] != '': new_contact = request.form['contact']
        else: new_contact = contact
        if "new_password" in request.form and request.form['new_password'] != '': 
            new_password = request.form['new_password']
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
            return jsonify({"msg":msg})
        
        # Hash old and new password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        
        hash = new_password + app.secret_key
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
                    return jsonify({'msg':msg})
                
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

@app.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)
    response = {"access_token":access_token}
    return response
## ADD forget_password FUNCTION AND ROUTE
##
##
##

############### END OF USERS API ###############

if __name__ == '__main__':
    app.run(
        # 'localhost',
        port=8000, 
        # debug=True
        )