from flask import Blueprint, render_template, request

from utils.password_rules import analyze_password
from utils.password_generator import generate_suggestions

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

            result["generated_passwords"] = generate_suggestions(
                password_text
            )

    return render_template(

        "password.html",

        page_title="Password Analyzer",

        page_subtitle="Analyze password strength without storing or transmitting your password.",

        result=result,

        password_text=password_text

    )