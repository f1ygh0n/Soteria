from flask import Blueprint, render_template, request

from utils.website_rules import analyze_website
from ai.website_ai import analyze_website_ai
from database.database import save_history

website_bp = Blueprint("website", __name__)


@website_bp.route("/website", methods=["GET", "POST"])
def website():

    result = None
    url = ""

    if request.method == "POST":

        url = request.form.get("url", "").strip()

        rules = analyze_website(url)

        ai = analyze_website_ai(rules)

        result = {

            **rules,

            "ai": ai,

            "ai_used": True

        }

    if result:

        save_history(

            module="Website Checker",

            score=result["risk_score"],

            verdict=result["quick_verdict"],

            summary=result["ai"]["summary"]

        )

    return render_template(
        "website.html",
        page_title="Website Checker",
        page_subtitle="Analyze websites for phishing and scams.",
        result=result,
        url=url
    )