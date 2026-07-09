import json
import os

from dotenv import load_dotenv
from google import genai

from ai.prompt_templates import CHAT_ANALYSIS_PROMPT

load_dotenv()


class ChatAI:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def analyze_chat(self, chat_text):

        prompt = f"""
{CHAT_ANALYSIS_PROMPT}

Conversation:

{chat_text}
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