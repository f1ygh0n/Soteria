from flask import Blueprint, render_template, request

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["GET", "POST"])
def chat():

    result = None
    chat_text = ""

    return render_template(
        "chat.html",
        page_title="Chat Scam Detector",
        page_subtitle="Detect scams in chats and conversations.",
        result=result,
        chat_text=chat_text
    )