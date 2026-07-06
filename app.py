from flask import Flask
from flask_session import Session

import os

# REMOVE THIS LINE BEFORE DEPLOYING TO PRODUCTION
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)

app.secret_key = "Jyot1r@ditya&Avid@an"

app.config["SESSION_TYPE"] = "filesystem"

Session(app)

from routes.home import home_bp
from routes.email import email_bp
from routes.gmail import gmail_bp

app.register_blueprint(home_bp)
app.register_blueprint(email_bp)
app.register_blueprint(gmail_bp)

if __name__ == "__main__":
    app.run(debug=True)