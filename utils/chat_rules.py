import re

SUSPICIOUS_KEYWORDS = [
    "otp",
    "verification code",
    "gift card",
    "steam card",
    "apple gift card",
    "google play card",
    "bitcoin",
    "crypto",
    "usdt",
    "ethereum",
    "wallet address",
    "investment",
    "refund",
    "bank account",
    "password",
    "login",
    "wire transfer",
    "upi",
    "paypal",
    "credit card",
    "debit card",
    "cvv",
    "pin"
]

URGENCY_KEYWORDS = [
    "urgent",
    "immediately",
    "right now",
    "within 24 hours",
    "today only",
    "act now",
    "last chance",
    "expires today",
    "hurry",
    "quick",
    "asap"
]

SECRECY_KEYWORDS = [
    "don't tell anyone",
    "keep this secret",
    "between us",
    "confidential",
    "do not tell",
    "don't inform anyone"
]

IMPERSONATION_KEYWORDS = [
    "customer support",
    "technical support",
    "bank representative",
    "microsoft support",
    "amazon support",
    "google support",
    "paypal support",
    "police",
    "government",
    "income tax department",
    "security team"
]

REMOTE_ACCESS_KEYWORDS = [
    "anydesk",
    "teamviewer",
    "rustdesk",
    "quick assist",
    "quickassist",
    "ultraviewer"
]

ROMANCE_KEYWORDS = [
    "i love you",
    "trust me",
    "send me money",
    "plane ticket",
    "medical emergency",
    "my dear",
    "my love"
]

PAYMENT_PATTERNS = [
    r"\$[0-9]+",
    r"₹\s?[0-9]+",
    r"\bupi\b",
    r"\bpayment\b",
    r"\bpay\b",
    r"\bsend money\b",
    r"\bbank transfer\b",
    r"\bwire transfer\b"
]

OTP_PATTERNS = [
    r"\botp\b",
    r"\bverification code\b",
    r"\b6[- ]?digit code\b",
    r"\bone time password\b",
    r"\bauthentication code\b"
]

EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

PHONE_PATTERN = r"\+?\d[\d\s\-]{7,}"

URL_PATTERN = r"https?://[^\s]+"

CRYPTO_PATTERN = [
    r"\b0x[a-fA-F0-9]{40}\b",
    r"\bbc1[a-zA-Z0-9]{20,}\b"
]


def analyze_chat_rules(chat_text):

    text = chat_text.lower()

    score = 0
    flags = []

    for word in SUSPICIOUS_KEYWORDS:

        if word in text:

            score += 8

            flags.append(f"keyword:{word}")

    for word in URGENCY_KEYWORDS:

        if word in text:

            score += 8

            flags.append("urgency")

            break

    for word in SECRECY_KEYWORDS:

        if word in text:

            score += 15

            flags.append("secrecy")

            break

    for word in IMPERSONATION_KEYWORDS:

        if word in text:

            score += 20

            flags.append("impersonation")

            break

    for word in REMOTE_ACCESS_KEYWORDS:

        if word in text:

            score += 20

            flags.append("remote_access")

            break

    for word in ROMANCE_KEYWORDS:

        if word in text:

            score += 15

            flags.append("romance")

            break

    payment_found = False

    for pattern in PAYMENT_PATTERNS:

        if re.search(pattern, text):

            payment_found = True

            break

    if payment_found:

        score += 15

        flags.append("payment_request")

    otp_found = False

    for pattern in OTP_PATTERNS:

        if re.search(pattern, text):

            otp_found = True

            break

    if otp_found:

        score += 20

        flags.append("otp_request")

    urls = re.findall(URL_PATTERN, text)

    if urls:

        score += 5

        flags.append("link_detected")

    if re.search(EMAIL_PATTERN, text):

        score += 5

        flags.append("email_detected")

    if re.search(PHONE_PATTERN, text):

        score += 5

        flags.append("phone_number")

    wallet_found = False

    for pattern in CRYPTO_PATTERN:

        if re.search(pattern, text):

            wallet_found = True

            break

    if wallet_found:

        score += 20

        flags.append("crypto_wallet")

    score = min(score, 100)

    if score >= 70:

        verdict = "HIGH"

    elif score >= 35:

        verdict = "SUSPICIOUS"

    else:

        verdict = "SAFE"

    return {

        "risk_score": score,

        "flags": flags,

        "quick_verdict": verdict

    }