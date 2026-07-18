from flask import Blueprint, render_template

from database.database import get_history

from database.database import save_history

history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
def history():

    scans = get_history()

    return render_template(

        "history.html",

        page_title="Scan History",

        page_subtitle="View previous security scans and their results.",

        scans=scans

    )