import ipaddress
import requests

from urllib.parse import urlparse

from utils.domain_utils import (
    get_domain,
    get_domain_age,
    detect_typosquatting
)


SUSPICIOUS_KEYWORDS = [

    "login",
    "verify",
    "secure",
    "account",
    "update",
    "confirm",
    "bank",
    "password",
    "signin",
    "wallet"

]


def analyze_website(url):

    flags = []

    risk_score = 0

    if not url.startswith(("http://", "https://")):

        url = "https://" + url

    try:

        parsed = urlparse(url)

        domain = get_domain(url)

    except Exception:

        return {

            "risk_score": 100,

            "quick_verdict": "HIGH",

            "flags": [

                "Invalid URL"

            ]

        }

    if parsed.scheme != "https":

        risk_score += 25

        flags.append("Website does not use HTTPS")

    else:

        flags.append("HTTPS enabled")

    try:

        ipaddress.ip_address(domain)

        risk_score += 30

        flags.append("Website uses an IP address instead of a domain")

    except ValueError:

        pass

    if len(url) > 75:

        risk_score += 10

        flags.append("Very long URL")

    lowered = url.lower()

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in lowered:

            risk_score += 10

            flags.append(f"Contains suspicious keyword: {keyword}")

    age = get_domain_age(domain)

    if age is None:

        flags.append("Unable to determine domain age")

    elif age < 30:

        risk_score += 25

        flags.append(f"Recently registered domain ({age} days old)")

    elif age < 180:

        risk_score += 10

        flags.append(f"Relatively new domain ({age} days old)")

    lookalike = detect_typosquatting(domain)

    if lookalike:

        legit, similarity = lookalike

        risk_score += 35

        flags.append(
            f"Looks similar to {legit} ({similarity:.0f}% similarity)"
        )

    try:

        response = requests.get(

            url,

            timeout=5,

            allow_redirects=True,

            headers={

                "User-Agent": "Soteria Website Scanner"

            }

        )

        if len(response.history) >= 3:

            risk_score += 10

            flags.append("Multiple redirects detected")

    except Exception:

        risk_score += 15

        flags.append("Website could not be reached")

    risk_score = min(risk_score, 100)

    if risk_score >= 70:

        verdict = "HIGH"

    elif risk_score >= 35:

        verdict = "SUSPICIOUS"

    else:

        verdict = "SAFE"

    return {

        "risk_score": risk_score,

        "quick_verdict": verdict,

        "flags": flags

    }