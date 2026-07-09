from flask import Blueprint, render_template

password_bp = Blueprint("password", __name__)


@password_bp.route("/password")
def password():

    return render_template(

        "password.html",

        page_title="Password Analyzer",

        page_subtitle="Analyze password strength without storing or transmitting your password."

    )