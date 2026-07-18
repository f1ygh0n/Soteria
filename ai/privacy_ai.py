import os
import json

from google import genai

from dotenv import load_dotenv

from ai.prompt_templates import PRIVACY_ANALYSIS_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_privacy(findings):

    if not findings:

        return {

            "summary": "No sensitive information was detected. The scanned content appears safe.",

            "risk_level": "Very Low",

            "recommendations": [

                "Continue following good security practices.",

                "Avoid storing passwords or API keys in plain text.",

                "Review sensitive files regularly."

            ]

        }

    findings_text = "\n".join(

        f"{item['type']}: {item['count']}"

        for item in findings

    )

    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=PRIVACY_ANALYSIS_PROMPT.format(
            findings=findings_text
        )

    )

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    data = json.loads(text)

    return {

        "summary": data["summary"],

        "risk_level": data["risk_level"],

        "recommendations": data["recommendations"]

    }