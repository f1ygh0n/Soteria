from flask import Blueprint, redirect, session

from gmail.auth import flow

from flask import request, url_for

from google.oauth2.credentials import Credentials

from google.oauth2.credentials import Credentials

from gmail.client import GmailClient

from flask import jsonify

gmail_bp = Blueprint("gmail", __name__)


@gmail_bp.route("/gmail/login")
def gmail_login():

    authorization_url, state = flow.authorization_url(

        access_type="offline",

        include_granted_scopes="true",

        prompt="consent"

    )

    session["state"] = state

    return redirect(authorization_url)

@gmail_bp.route("/oauth2callback")
def oauth2callback():

    flow.fetch_token(

        authorization_response=request.url

    )

    credentials = flow.credentials

    session["credentials"] = {

        "token": credentials.token,

        "refresh_token": credentials.refresh_token,

        "token_uri": credentials.token_uri,

        "client_id": credentials.client_id,

        "client_secret": credentials.client_secret,

        "scopes": credentials.scopes

    }

    return redirect(url_for("email.email"))

@gmail_bp.route("/gmail/list")
def gmail_list():

    if "credentials" not in session:

        return jsonify([])

    credentials = Credentials(**session["credentials"])

    gmail = GmailClient(credentials)

    emails = gmail.get_recent_emails()

    return jsonify(emails)

@gmail_bp.route("/gmail/email/<message_id>")
def gmail_email(message_id):

    credentials = Credentials(
        **session["credentials"]
    )

    gmail = GmailClient(credentials)

    email_data = gmail.get_email_data(message_id)

    return jsonify(email_data)