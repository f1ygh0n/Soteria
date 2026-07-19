import os
import json

from google import genai
from google.genai import types

from dotenv import load_dotenv

from ai.prompt_templates import DEEPFAKE_ANALYSIS_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def detect_ai_image(path):

    with open(path, "rb") as f:
        image = f.read()

    response = client.models.generate_content(

        model="gemini-2.5-flash",
        
        contents=[
            DEEPFAKE_ANALYSIS_PROMPT,
            types.Part.from_bytes(
                data=image,
                mime_type="image/jpeg"
            )
        ]
    )

    text = response.text.strip()
    
    text = text.replace("```json", "")
    text = text.replace("```", "")

    data = json.loads(text)

    return {

        "success": True,

        "probability": data["probability"],

        "label": data["verdict"],

        "reason": data["reason"]

    }