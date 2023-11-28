from flask import Flask, render_template, redirect, request, jsonify, session, send_file
from pymysql import connect
from pymysql.cursors import re, DictCursor
import numpy as np
import cv2
from PIL import Image
import io
import dotenv
import os
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

if __name__ == '__main__':
    app.run('localhost',port=6000, debug=True)