from flask import Flask, render_template, redirect, request, jsonify, session, send_file, Blueprint
from pymysql import connect
from pymysql.cursors import re, DictCursor
import numpy as np
import cv2
from PIL import Image
import io
import dotenv
import os
import base64
# Load the environment variables
dotenv.load_dotenv()

history_bp = Blueprint('history',__name__)
# Change this to your secret key (it can be anything, it's for extra protection)
history_bp.secret_key = os.getenv("SECRET_KEY")
# history_bp.config["SESSION_PERMANENT"] = False
# history_bp.config["SESSION_TYPE"] = "filesystem"


# Connect to the database
connection = connect(host=os.getenv("DATABASE_URL"),
                    user=os.getenv("USER"),
                    password=os.getenv("PASSWORD"),
                    database=os.getenv("DATABASE_NAME"),
                    cursorclass=DictCursor,
                    # port=int(os.getenv("DATABASE_PORT"))
                    )

# @history_bp.route("/get_history", methods=["GET"])
# def get_history():
#     try:
#         if request.method == 'GET':
#             if session.get("loggedin") is False:
#                 return jsonify({'msg': "You are not logged in"}), 400

#             user_id = session.get('user_id')

#             # Retrieving data from the database
#             connection.ping(reconnect=True)
#             with connection.cursor() as cursor:
#                 cursor.execute(f"SELECT * FROM `history` WHERE `user_id` = {user_id}")
#                 data = cursor.fetchall()

#             if not data:
#                 return jsonify({'msg': 'No history found for the user'}), 404

#             # Formatting retrieved data
#             history = {str(i): {
#                 'history_id': data[i]['history_id'],
#                 'user_id': data[i]['user_id'],
#                 'stress_id': data[i]['stress_id'],
#                 'date_transaction': data[i]['date_transaction'],
#                 'image_name': data[i]['image_name']
#             } for i in range(len(data))}

#             msg = 'Successfully retrieved history'
#             return jsonify({'msg': msg, 'history': history}), 200

#         msg = 'Invalid request'
#         return jsonify({'msg': msg}), 400
#     except Exception as e:
#         return str(e), 500

## get all history entries (might only get 6)
@history_bp.route("/get_history_with_images", methods=["GET"])
def get_history_with_images():
    try:
        # Fetch history data and image data from the database
        if session.get("loggedin") is False:
            return jsonify({'msg': "You are not logged in"}), 400

        user_id = request.headers.get('User-Id')  # Get user ID from headers
        if not user_id:
            return jsonify({'msg': "User ID not provided in headers"}), 400

        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `history` WHERE `user_id` = %s", (user_id,))
            history_data = cursor.fetchall()

            cursor.execute("SELECT rice_image FROM history WHERE user_id = %s", (user_id,))
            image_data = cursor.fetchall()
        if len(history_data) < 6:
            LIMIT = len(history_data)
        else:
            LIMIT = 6
        history_data = history_data[::-1][:LIMIT]
        image_data = image_data[::-1][:LIMIT]
        connection.commit()
        

        # Combine history and image data
        history_with_images = []
        for i, history_entry in enumerate(history_data):
            entry = {
                'history_id': history_entry['history_id'],
                'user_id': history_entry['user_id'],
                'stress_id': history_entry['stress_id'],
                'date_transaction': history_entry['date_transaction'],
                'image_name': history_entry['image_name'],
                'scan_num':i+1
            }

            # If there is corresponding image data, include it
            if i < len(image_data):
                # image = Image.frombytes("RGB", (224, 224), image_data[i]['rice_image'])
                # image_io = io.BytesIO()
                # image.save(image_io, 'JPEG')
                # image_io.seek(0)

                # # Convert binary image data to base64-encoded string
                # entry['image'] = base64.b64encode(image_io.getvalue()).decode('utf-8')
                # Decode the string
                entry['image'] = base64.b64encode(image_data[i]['rice_image']).decode('utf-8')
            history_with_images.append(entry)
            # print(history_with_images)

        msg = 'Successfully retrieved history with images'
        return jsonify({'msg': msg, 'history_with_images': history_with_images}), 200

    except Exception as e:
        return str(e), 500

## get history entry of one only
@history_bp.route("/get_history_entry/<int:history_id>", methods=["GET"])
def get_history_entry(history_id):
    try:
        # Fetch history data and image data for a specific history entry
        if session.get("loggedin") is False:
            return jsonify({'msg': "You are not logged in"}), 400

        user_id = request.headers.get('User-Id')
        stress_id = request.headers.get('Stress-Id')
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `rice_stress` WHERE `stress_id`=%s", (stress_id,))
            rice_stress_data = cursor.fetchone()

            cursor.execute("SELECT rice_image FROM history WHERE user_id = %s AND `history_id`=%s", (user_id, history_id,))
            image_data = cursor.fetchone()
            entry = {
            # 'history_id': history_data['history_id'],
            # 'user_id': rice_stress_data['user_id'],
            'stress_type': rice_stress_data['stress_type'],
            'stress_id': rice_stress_data['stress_id'],
            # 'date_transaction': rice_stress_data['date_transaction'],
            'stress_name': rice_stress_data['stress_name'],
            'stress_level': rice_stress_data['stress_level'],
            'description': rice_stress_data['description'],
            'recommendation': rice_stress_data['recommendation'],
            'recommendation_src': rice_stress_data['recommendation_src'],
            'description_src': rice_stress_data['description_src'],
            }

                # If there is corresponding image data, include it
            if image_data:
                entry['image'] = base64.b64encode(image_data['rice_image']).decode('utf-8')

                msg = f'Successfully retrieved history entry with history_id {history_id}'
                return jsonify({'msg': msg, 'history_entry': entry}), 200
            else:
                return 'History entry not found', 404

    except Exception as e:
        return str(e), 500


# if __name__ == '__main__':
#     history_bp.run('localhost',port=6000, debug=True)