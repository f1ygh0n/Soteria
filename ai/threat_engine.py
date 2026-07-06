import re

SUSPICIOUS_KEYWORDS = [
    "urgent", "verify", "password", "login", "suspended",
    "click here", "bank", "paypal", "account locked",
    "otp", "credit card"
]

FAKE_DOMAIN_PATTERNS = [
    r".*-secure\..*",
    r".*-verify\..*",
    r".*-login\..*",
    r".*paypal.*(?!\.com)",
    r".*bank.*\.xyz"
]


def analyze_email_rules(email_text: str):

    text = email_text.lower()

    score = 0
    flags = []

    # keyword detection
    for word in SUSPICIOUS_KEYWORDS:
        if word in text:
            score += 10
            flags.append(f"keyword:{word}")

    # URL detection
    urls = re.findall(r"https?://[^\s]+", text)
    if urls:
        score += 20
        flags.append("url_detected")

        for url in urls:
            for pattern in FAKE_DOMAIN_PATTERNS:
                if re.search(pattern, url):
                    score += 30
                    flags.append("suspicious_domain")

    # urgency detection
    if "immediately" in text or "24 hours" in text:
        score += 15
        flags.append("urgency_tactic")

    # final classification
    if score >= 70:
        level = "HIGH"
    elif score >= 30:
        level = "SUSPICIOUS"
    else:
        level = "SAFE"

    return {
        "risk_score": min(score, 100),
        "flags": flags,
        "quick_verdict": level
    }