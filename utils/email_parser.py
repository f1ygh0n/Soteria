from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
import re


def parse_eml(file):

    message = BytesParser(policy=policy.default).parse(file)

    body = ""

    if message.is_multipart():

        for part in message.walk():

            if part.get_content_type() == "text/plain":

                body += part.get_content()

    else:

        body = message.get_content()

    return {

        "from": parseaddr(message.get("From", ""))[1],

        "to": parseaddr(message.get("To", ""))[1],

        "reply_to": parseaddr(message.get("Reply-To", ""))[1],

        "return_path": parseaddr(message.get("Return-Path", ""))[1],

        "subject": message.get("Subject", ""),

        "date": message.get("Date", ""),

        "body": body,

        "headers": dict(message.items())

    }


def parse_pasted_email(text):

    data = {

        "from": "",

        "to": "",

        "reply_to": "",

        "return_path": "",

        "subject": "",

        "date": "",

        "body": text,

        "headers": {}

    }

    patterns = {

        "from": r"^From:\s*(.+)$",

        "to": r"^To:\s*(.+)$",

        "subject": r"^Subject:\s*(.+)$",

        "reply_to": r"^Reply-To:\s*(.+)$",

        "date": r"^Date:\s*(.+)$"

    }

    for key, pattern in patterns.items():

        match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)

        if match:

            value = match.group(1).strip()

            if key in ("from", "to", "reply_to"):

                value = parseaddr(value)[1]

            data[key] = value

    return data