from flask import Blueprint, render_template, request, jsonify

from ai.chat_ai import ChatAI
from utils.chat_rules import analyze_chat_rules
from utils.chat_ocr import extract_chat_text
from database.database import save_history

chat_bp = Blueprint("chat", __name__)

ai = ChatAI()

@chat_bp.route("/parse-chat-image", methods=["POST"])
def parse_chat_image():

    uploaded_image = request.files.get("chat_image")

    if not uploaded_image:

        return jsonify({

            "success": False,

            "message": "No image uploaded."

        }), 400

    try:

        chat_text = extract_chat_text(uploaded_image)

        return jsonify({

            "success": True,

            "chat_text": chat_text

        })

    except Exception as e:

        import traceback
        traceback.print_exc()

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500

@chat_bp.route("/chat", methods=["GET", "POST"])
def chat():

    result = None
    chat_text = ""

    if request.method == "POST":

        uploaded_image = request.files.get("chat_image")

        chat_text = request.form.get(
            "chat_text",
            ""
        ).strip()

        if (
            uploaded_image
            and uploaded_image.filename
        ):

            try:

                chat_text = extract_chat_text(uploaded_image)

            except Exception as e:

                result = {

                    "rules": {

                        "risk_score": 0,

                        "quick_verdict": "ERROR",

                        "flags": []

                    },

                    "ai_used": False,

                    "ai": {

                        "threat_level": "ERROR",

                        "summary": f"Could not read the uploaded screenshot.\n\n{e}"

                    }

                }

        if chat_text and result is None:

            rules = analyze_chat_rules(chat_text)

            result = {

                "rules": rules,

                "ai_used": False,

                "ai": None

            }

            if rules["risk_score"] >= 85:

                result["ai"] = {

                    "threat_level": rules["quick_verdict"],

                    "summary": (
                        "This conversation contains multiple high-confidence "
                        "scam indicators. AI verification was unnecessary."
                    ),

                    "reasons": [],

                    "recommendation": (
                        "Do not respond, click any links, or send money. "
                        "Block and report the sender."
                    )

                }

            else:

                try:

                    ai_result = ai.analyze_chat(chat_text)

                    result["ai_used"] = True

                    result["ai"] = ai_result

                except Exception:

                    result["ai"] = {

                        "threat_level": rules["quick_verdict"],

                        "summary": (
                            "AI analysis is temporarily unavailable. "
                            "Showing the local rule engine's assessment."
                        ),

                        "reasons": [],

                        "recommendation": (
                            "Exercise caution and verify the sender "
                            "through an independent source."
                        )

                    }

    if result:

        save_history(

            module="Chat Scam Detector",

            score=rules["risk_score"],

            verdict=rules["quick_verdict"],

            summary=result["ai"]["summary"]

        )

    return render_template(

        "chat.html",

        page_title="Chat Scam Detector",

        page_subtitle="Detect scams in chats and conversations.",

        result=result,

        chat_text=chat_text

    )