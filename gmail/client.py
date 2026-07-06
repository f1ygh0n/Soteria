from googleapiclient.discovery import build

import base64
from bs4 import BeautifulSoup

class GmailClient:

    def __init__(self, credentials):

        self.service = build(
            "gmail",
            "v1",
            credentials=credentials
        )

    def get_recent_emails(self, max_results=10):

        results = self.service.users().messages().list(
            userId="me",
            maxResults=max_results
        ).execute()

        messages = results.get("messages", [])

        emails = []

        for message in messages:

            msg = self.service.users().messages().get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"]
            ).execute()

            headers = msg["payload"]["headers"]

            subject = ""
            sender = ""
            date = ""

            for header in headers:

                if header["name"] == "Subject":
                    subject = header["value"]

                elif header["name"] == "From":
                    sender = header["value"]

                elif header["name"] == "Date":
                    date = header["value"]

            emails.append({

                "id": message["id"],

                "subject": subject,

                "from": sender,

                "date": date

            })

        return emails
    
    def get_email_body(self, message_id):

        message = self.service.users().messages().get(
            userId="me",
            id=message_id,
            format="full"
        ).execute()

        def extract(parts):

            for part in parts:

                mime = part.get("mimeType", "")

                if mime == "text/plain":

                    data = part["body"].get("data")

                    if data:

                        return base64.urlsafe_b64decode(
                            data
                        ).decode("utf-8", errors="ignore")

                if mime == "text/html":

                    data = part["body"].get("data")

                    if data:

                        html = base64.urlsafe_b64decode(
                            data
                        ).decode("utf-8", errors="ignore")

                        return BeautifulSoup(
                            html,
                            "html.parser"
                        ).get_text("\n")

                if "parts" in part:

                    result = extract(part["parts"])

                    if result:

                        return result

            return None

        payload = message["payload"]

        if "parts" in payload:

            body = extract(payload["parts"])

        else:

            data = payload["body"].get("data", "")

            body = base64.urlsafe_b64decode(
                data
            ).decode("utf-8", errors="ignore")

        return body