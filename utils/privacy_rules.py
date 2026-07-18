import re


PATTERNS = {

    "Email Addresses": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),

    "Phone Numbers": re.compile(
        r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,5}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{4}"
    ),

    "Google API Keys": re.compile(
        r"AIza[0-9A-Za-z\-_]{35}"
    ),

    "OpenAI API Keys": re.compile(
        r"sk-[A-Za-z0-9]{20,}"
    ),

    "Hugging Face Tokens": re.compile(
        r"hf_[A-Za-z0-9]{30,}"
    ),

    "GitHub Tokens": re.compile(
        r"gh[pousr]_[A-Za-z0-9_]{30,255}"
    ),

    "AWS Access Keys": re.compile(
        r"AKIA[0-9A-Z]{16}"
    ),

    "JWT Tokens": re.compile(
        r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
    ),

    "Private Keys": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),

    "IPv4 Addresses": re.compile(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ),

    "Credit Card Numbers": re.compile(
        r"\b(?:\d[ -]*?){13,16}\b"
    ),

    "Password Assignments": re.compile(
        r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|apikey)\b\s*[:=]\s*[\"']?.+"
    ),
}


def mask(text):

    text = str(text).strip()

    if len(text) <= 8:
        return "*" * len(text)

    return text[:4] + "••••••" + text[-4:]


def calculate_risk(findings):

    total = sum(item["count"] for item in findings)

    score = 100

    for item in findings:

        t = item["type"]
        c = item["count"]

        if "Password" in t:
            score -= c * 15

        elif "API" in t:
            score -= c * 15

        elif "Private Key" in t:
            score -= c * 25

        elif "JWT" in t:
            score -= c * 15

        elif "Credit Card" in t:
            score -= c * 20

        elif "AWS" in t:
            score -= c * 20

        else:
            score -= c * 5

    score = max(0, min(score, 100))

    if score >= 90:
        verdict = "Very Safe"

    elif score >= 75:
        verdict = "Low Risk"

    elif score >= 55:
        verdict = "Moderate Risk"

    elif score >= 35:
        verdict = "High Risk"

    else:
        verdict = "Critical Risk"

    return score, verdict, total


def analyze_text(text):

    findings = []

    for name, pattern in PATTERNS.items():

        matches = pattern.findall(text)

        if not matches:
            continue

        examples = []

        for match in matches:

            if isinstance(match, tuple):
                match = match[0]

            examples.append(mask(match))

        findings.append({

            "type": name,

            "count": len(matches),

            "examples": examples[:3]

        })

    score, verdict, total = calculate_risk(findings)

    if total == 0:

        summary = (
            "No common sensitive information was detected."
        )

    else:

        summary = (
            f"Detected {total} potentially sensitive item(s) "
            f"across {len(findings)} category(s)."
        )

    return {

        "score": score,

        "verdict": verdict,

        "summary": summary,

        "findings": findings,

        "ai_input": [
            {
                "type": item["type"],
                "count": item["count"]
            }
            for item in findings
        ]

    }