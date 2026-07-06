import json
import os

from dotenv import load_dotenv
from google import genai

from ai.prompt_templates import EMAIL_ANALYSIS_PROMPT
from ai.threat_engine import analyze_email_rules

load_dotenv()

def should_use_ai(rules):

    return rules["risk_score"] < 85

class AIAnalyzer:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def analyze_email(self, email_text):

        prompt = f"""
{EMAIL_ANALYSIS_PROMPT}

Email:

{email_text}
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
    
