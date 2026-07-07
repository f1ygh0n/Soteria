import json
import os

from dotenv import load_dotenv
from google import genai

from ai.prompt_templates import WEBSITE_ANALYSIS_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_website_ai(evidence):

    prompt = WEBSITE_ANALYSIS_PROMPT + "\n\n"

    prompt += json.dumps(evidence, indent=2)

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return json.loads(text)

    except Exception as e:

        print("Website AI Error:", e)

        return {
            "threat_level": "UNKNOWN",
            "summary": "AI analysis unavailable."
        }