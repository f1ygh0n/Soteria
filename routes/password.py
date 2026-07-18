from flask import Blueprint, render_template, request

from utils.password_rules import analyze_password

from database.database import save_history

password_bp = Blueprint("password", __name__)


@password_bp.route("/password", methods=["GET", "POST"])
def password():

    result = None

    password_text = ""

    if request.method == "POST":

        password_text = request.form.get(
            "password",
            ""
        ).strip()

        if password_text:

            result = analyze_password(password_text)

    if result:

        save_history(

            module="Password Analyzer",

            score=result["score"],

            verdict=result["strength"],

            summary=(
                "; ".join(result["weaknesses"])
                if result["weaknesses"]
                else "No significant weaknesses detected."
            )

        )

    return render_template(

        "password.html",

        page_title="Password Analyzer",

        page_subtitle="Analyze password strength without storing or transmitting your password.",

        result=result,

        password_text=password_text

    )