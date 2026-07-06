from flask import Blueprint, render_template, request

website_bp = Blueprint("website", __name__)


@website_bp.route("/website", methods=["GET", "POST"])
def website():

    result = None
    url = ""

    if request.method == "POST":
        url = request.form.get("url", "")

    return render_template(
        "website.html",
        page_title="Website Checker",
        page_subtitle="Analyze URLs to spot fraud attempts.",
        url=url,
        result=result
    )