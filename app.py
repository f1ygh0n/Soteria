from flask import Flask
from flask_session import Session
from database.database import init_database

import whois
import os

# REMOVE THIS LINE BEFORE DEPLOYING TO PRODUCTION
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.config["SESSION_TYPE"] = "filesystem"

Session(app)

from routes.home import home_bp
from routes.email import email_bp
from routes.gmail import gmail_bp
from routes.website import website_bp
from routes.search import search_bp
from routes.chat import chat_bp
from routes.password import password_bp
from routes.deepfake import deepfake_bp
from routes.privacy import privacy_bp
from routes.history import history_bp

app.register_blueprint(home_bp)
app.register_blueprint(email_bp)
app.register_blueprint(gmail_bp)    
app.register_blueprint(website_bp)
app.register_blueprint(search_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(password_bp)
app.register_blueprint(deepfake_bp)
app.register_blueprint(privacy_bp)
app.register_blueprint(history_bp)

if __name__ == "__main__":
    init_database()
    app.run(debug=False) 