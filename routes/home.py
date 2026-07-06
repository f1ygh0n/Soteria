from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        page_title="Dashboard",
        page_subtitle="Monitor scans, threats and system activity."
    )