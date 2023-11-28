from flask import Flask
from routes.history import history_bp
from routes.recommendation import recommendation_bp
from routes.users import users_bp
import dotenv
import os

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(history_bp, url_prefix='/api/history')
app.register_blueprint(recommendation_bp, url_prefix='/api/recommendation')
app.register_blueprint(users_bp, url_prefix='/api/users')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))