import json
import os

from dotenv import load_dotenv
from google import genai

from ai.prompt_templates import EMAIL_ANALYSIS_PROMPT

load_dotenv()


def should_use_ai(rules):

    return rules["risk_score"] < 85


class AIAnalyzer:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def analyze_email(self, email_data):

        prompt = f"""
{EMAIL_ANALYSIS_PROMPT}

You are given a parsed email.

Treat ONLY the values below as the real metadata.

Do NOT guess the sender from the email body.

Email Metadata

From:
{email_data["from"]}

To:
{email_data["to"]}

Reply-To:
{email_data["reply_to"]}

Return-Path:
{email_data["return_path"]}

Subject:
{email_data["subject"]}

Date:
{email_data["date"]}

Body:
{email_data["body"]}

Rules:

- Never assume the recipient is the sender.
- If From is empty, say it is unavailable.
- Compare the sender domain with the brand mentioned.
- Use Reply-To and Return-Path when relevant.
- Ignore quoted emails unless they contain phishing evidence.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return json.loads(text)