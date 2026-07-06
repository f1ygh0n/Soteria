from google_auth_oauthlib.flow import Flow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

flow = Flow.from_client_secrets_file(
    "credentials.json",
    scopes=SCOPES
)

flow.redirect_uri = "http://127.0.0.1:5000/oauth2callback"