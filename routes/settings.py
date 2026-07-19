from flask import Blueprint, render_template, request, redirect, url_for

from database.database import clear_history

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():

    if request.method == "POST":

        clear_history()

        return redirect(url_for("settings.settings"))

    return render_template(

        "settings.html",

        page_title="Settings",

        page_subtitle="Customize Soteria, manage your data and view application information."

    )