from flask import Blueprint, render_template, request
from flask import jsonify

from email import policy
from email.parser import BytesParser

from ai.ai_analyzer import AIAnalyzer, should_use_ai
from ai.threat_engine import analyze_email_rules

email_bp = Blueprint("email", __name__)

ai = AIAnalyzer()

@email_bp.route("/parse-eml", methods=["POST"])
def parse_eml():

    uploaded_file = request.files.get("email_file")

    if not uploaded_file:

        return jsonify({
            "success": False,
            "message": "No file uploaded."
        }), 400

    try:

        msg = BytesParser(policy=policy.default).parse(
            uploaded_file.stream
        )

        sender = msg.get("From", "")
        recipient = msg.get("To", "")
        subject = msg.get("Subject", "")
        date = msg.get("Date", "")

        body = ""

        if msg.is_multipart():

            for part in msg.walk():

                if (
                    part.get_content_type() == "text/plain"
                    and "attachment"
                    not in str(part.get("Content-Disposition", "")).lower()
                ):

                    body = part.get_content()

                    break

            if not body:

                for part in msg.walk():

                    if part.get_content_type() == "text/html":

                        body = part.get_content()

                        break

        else:

            body = msg.get_content()

        email_text = f"""
From: {sender}
To: {recipient}
Subject: {subject}
Date: {date}

{body}
""".strip()

        return jsonify({

            "success": True,

            "email_text": email_text

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500

@email_bp.route("/email", methods=["GET", "POST"])
def email():

    result = None
    email_text = ""

    if request.method == "POST":

        uploaded_file = request.files.get("email_file")
        email_text = request.form.get("email_text", "").strip()

        if (
            uploaded_file
            and uploaded_file.filename
            and uploaded_file.filename.lower().endswith(".eml")
        ):

            try:

                msg = BytesParser(policy=policy.default).parse(
                    uploaded_file.stream
                )

                sender = msg.get("From", "")
                recipient = msg.get("To", "")
                subject = msg.get("Subject", "")
                date = msg.get("Date", "")

                body = ""

                if msg.is_multipart():

                    for part in msg.walk():

                        if (
                            part.get_content_type() == "text/plain"
                            and "attachment"
                            not in str(part.get("Content-Disposition", "")).lower()
                        ):
                            body = part.get_content()
                            break

                    if not body:

                        for part in msg.walk():

                            if part.get_content_type() == "text/html":

                                body = part.get_content()
                                break

                else:

                    body = msg.get_content()

                email_text = f"""
                    From: {sender}
                    To: {recipient}
                    Subject: {subject}
                    Date: {date}

                    {body}
                    """.strip()

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
                        "summary": f"Could not parse .eml file.\n\n{e}"
                    }
                }

        if email_text and result is None:

            rules = analyze_email_rules(email_text)

            result = {
                "rules": rules,
                "ai_used": False,
                "ai": None
            }

            if should_use_ai(rules):

                try:

                    ai_result = ai.analyze_email(email_text)

                    result["ai_used"] = True
                    result["ai"] = ai_result

                except Exception:

                    result["ai"] = {
                        "threat_level": rules["quick_verdict"],
                        "summary": (
                            "AI analysis is temporarily unavailable. "
                            "Showing the local security engine's assessment."
                        )
                    }

            else:

                result["ai"] = {
                    "threat_level": rules["quick_verdict"],
                    "summary": (
                        "This email contains multiple high-confidence phishing "
                        "indicators. The local security engine determined that "
                        "AI verification was unnecessary."
                    )
                }

    return render_template(
        "email.html",
        page_title="Email Scanner",
        page_subtitle="Analyze suspicious emails using AI.",
        email_text=email_text,
        result=result
    )