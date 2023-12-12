from flask import Flask,jsonify,session,request
from routes.history import history_bp
from routes.recommendation import recommendation_bp
from routes.users import users_bp
import dotenv
import os
from flask_mail import Mail, Message
from flask_cors import CORS
import random
import asyncio
import aiohttp
from datetime import timedelta

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config["SESSION_TYPE"] = "filesystem"
EMAIL = os.getenv("MAIL_USERNAME")
app.config['MAIL_SERVER']= os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] =  os.getenv("MAIL_PORT")
app.config['MAIL_USERNAME'] =  EMAIL
app.config['MAIL_PASSWORD'] =  os.getenv("MAIL_PASSWORD")
# app.config['MAIL_USE_TLS'] =  os.getenv("MAIL_USE_TLS")
app.config['MAIL_USE_SSL'] =  os.getenv("MAIL_USE_SSL")
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
mail = Mail(app)
CORS(app)

# jwt = JWTManager(app)

@app.route('/api')
def index():
    return jsonify({'msg':'skanin API is now online'}), 200

# Register blueprints
app.register_blueprint(history_bp, url_prefix='/api/history')
app.register_blueprint(recommendation_bp, url_prefix='/api/recommendation')
app.register_blueprint(users_bp, url_prefix='/api/users')

# @app.route('/api/otp')
# def otp():
#     msg = ''
    
#     return jsonify({'msg':msg})

@app.route("/api/send_email", methods=['POST'])
async def send_email():
    data = request.get_json()
    email = data.get('email')
    message = data.get('message')

    # Add your email sending logic here
    ## APPLY OTP TO ACCOUNT 
    if session['email'] != None:
        OTP = os.getenv("SECRET_KEY").split(',')[random.randint(0,100)]
        session['OTP'] = OTP
        msg = Message( 
                    'OTP for Skanin',
                    sender = EMAIL, 
                    recipients = [email] 
                    ) 
        msg.body = message
        mail.send(msg) 
        return jsonify({'msg':"message send"}), 200
    return jsonify({'msg':'Error in sending OTP'}), 400
    # return "Email sent", 200

async def send_otp(email):
    OTP = os.getenv("SECRET_KEY").split(',')[random.randint(0, 100)]
    session['OTP'] = OTP

    msg = f'This is your one-time password (OTP): {OTP}. Please enter it in Skanin. If you did not request an OTP, please ignore this message.'

    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5000/api/send_email', json={'email': email, 'message': msg}) as response:
            return await response.text()

def otp():
    if session.get('email') is not None:
        asyncio.run(send_otp(session['email']))
        return jsonify({'msg': 'OTP sent successfully'}), 200
    return jsonify({'msg': 'Error in sending OTP'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))