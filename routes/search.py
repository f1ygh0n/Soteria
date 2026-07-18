from flask import Blueprint, render_template, request

search_bp = Blueprint("search", __name__)

PAGES = [
    {
        "name": "Dashboard",
        "description": "Overview of your cybersecurity tools.",
        "keywords": ["dashboard", "home"],
        "url": "/"
    },
    {
        "name": "Email Scanner",
        "description": "Analyze suspicious emails using AI and rule-based detection.",
        "keywords": ["email", "mail", "gmail", "scanner"],
        "url": "/email"
    },
    {
        "name": "Website Checker",
        "description": "Analyze URLs for phishing, HTTPS, lookalike domains and more.",
        "keywords": ["website", "url", "domain", "link", "phishing"],
        "url": "/website"
    },
    {
        "name": "Chat Detector",
        "description": "Detect scams in chats and conversations.",
        "keywords": ["chat", "message"],
        "url": "/chat"
    },
    {
        "name": "Password Analyzer",
        "description": "Analyze password strength without storing or transmitting your password.",
        "keywords": ["password"],
        "url": "/password"
    },
    {
        "name": "Deepfake Detector",
        "description": "Analyze uploaded images for visual inconsistencies commonly associated with AI-generated or manipulated content.",
        "keywords": ["deepfake", "image"],
        "url": "/deepfake"
    },
    {
        "name": "Privacy Scanner",
        "description": "Discover exposed personal information and privacy risks.",
        "keywords": ["privacy"],
        "url": "/privacy"
    }
]


@search_bp.route("/search")
def search():

    query = request.args.get("q", "").strip().lower()

    results = []

    if query:

        for page in PAGES:

            text = (
                page["name"] + " " +
                page["description"] + " " +
                " ".join(page["keywords"])
            ).lower()

            if query in text:
                results.append(page)

    return render_template(
        "search.html",
        page_title="Search Results",
        page_subtitle="Look for modules within Soteria.",
        query=query,
        results=results
    )