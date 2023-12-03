from flask import Flask,jsonify
from routes.history import history_bp
from routes.recommendation import recommendation_bp
from routes.users import users_bp
import dotenv
import os
from flask_cors import CORS

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
CORS(app)

# jwt = JWTManager(app)

@app.route('/api')
def index():
    return jsonify({'msg':'skanin API is now online'}), 200

# Register blueprints
app.register_blueprint(history_bp, url_prefix='/api/history')
app.register_blueprint(recommendation_bp, url_prefix='/api/recommendation')
app.register_blueprint(users_bp, url_prefix='/api/users')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))