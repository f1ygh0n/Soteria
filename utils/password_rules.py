import math
import re

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "123456789",
    "1234567890",
    "qwerty",
    "qwerty123",
    "admin",
    "welcome",
    "football",
    "dragon",
    "monkey",
    "abc123",
    "letmein",
    "iloveyou",
    "login",
    "master",
    "root"
}

KEYBOARD_PATTERNS = [
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "123456",
    "654321",
    "qazwsx",
    "1q2w3e"
]

SEQUENCES = [
    "abcdefghijklmnopqrstuvwxyz",
    "0123456789"
]


def calculate_entropy(password):

    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"[0-9]", password):
        charset += 10

    if re.search(r"[^a-zA-Z0-9]", password):
        charset += 32

    if charset == 0:
        return 0

    return round(len(password) * math.log2(charset), 1)


def has_sequence(password):

    password = password.lower()

    for sequence in SEQUENCES:

        for i in range(len(sequence) - 2):

            part = sequence[i:i + 3]

            if part in password:
                return True

            if part[::-1] in password:
                return True

    return False


def estimate_crack_time(entropy):

    if entropy < 28:
        return "Instantly"

    elif entropy < 36:
        return "Minutes"

    elif entropy < 45:
        return "Hours"

    elif entropy < 55:
        return "Days"

    elif entropy < 65:
        return "Months"

    elif entropy < 75:
        return "Years"

    elif entropy < 90:
        return "Centuries"

    return "Practically impossible with current technology"


def analyze_password(password):

    score = 0

    weaknesses = []

    suggestions = []

    length = len(password)

    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_number = bool(re.search(r"[0-9]", password))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9]", password))

    common_password = password.lower() in COMMON_PASSWORDS

    keyboard_pattern = any(
        pattern in password.lower()
        for pattern in KEYBOARD_PATTERNS
    )

    sequential = has_sequence(password)

    repeated = bool(
        re.search(r"(.)\1{2,}", password)
    )

    if length >= 16:
        score += 30

    elif length >= 12:
        score += 20

    elif length >= 8:
        score += 10

    else:

        weaknesses.append(
            "Password is too short."
        )

        suggestions.append(
            "Use at least 12 characters."
        )

    if has_upper:
        score += 10
    else:
        suggestions.append(
            "Add uppercase letters."
        )

    if has_lower:
        score += 10
    else:
        suggestions.append(
            "Add lowercase letters."
        )

    if has_number:
        score += 10
    else:
        suggestions.append(
            "Add numbers."
        )

    if has_symbol:
        score += 15
    else:
        suggestions.append(
            "Add special characters."
        )

    if common_password:

        score -= 40

        weaknesses.append(
            "This password appears in a list of common passwords."
        )

        suggestions.append(
            "Avoid common passwords."
        )

    if keyboard_pattern:

        score -= 15

        weaknesses.append(
            "Contains predictable keyboard patterns."
        )

        suggestions.append(
            "Avoid keyboard sequences like qwerty or 123456."
        )

    if sequential:

        score -= 10

        weaknesses.append(
            "Contains sequential characters."
        )

    if repeated:

        score -= 10

        weaknesses.append(
            "Contains repeated characters."
        )

    score = max(
        0,
        min(score, 100)
    )

    if score >= 81:

        strength = "Excellent"

    elif score >= 61:

        strength = "Strong"

    elif score >= 41:

        strength = "Fair"

    elif score >= 21:

        strength = "Weak"

    else:

        strength = "Very Weak"

    entropy = calculate_entropy(password)

    crack_time = estimate_crack_time(entropy)

    checks = [

        {
            "name": "12+ Characters",
            "passed": length >= 12
        },

        {
            "name": "Uppercase Letter",
            "passed": has_upper
        },

        {
            "name": "Lowercase Letter",
            "passed": has_lower
        },

        {
            "name": "Numbers",
            "passed": has_number
        },

        {
            "name": "Special Characters",
            "passed": has_symbol
        },

        {
            "name": "Not a Common Password",
            "passed": not common_password
        },

        {
            "name": "No Keyboard Patterns",
            "passed": not keyboard_pattern
        },

        {
            "name": "No Sequential Characters",
            "passed": not sequential
        },

        {
            "name": "No Repeated Characters",
            "passed": not repeated
        }

    ]

    return {

        "score": score,

        "strength": strength,

        "length": length,

        "entropy": entropy,

        "crack_time": crack_time,

        "checks": checks,

        "weaknesses": weaknesses,

        "suggestions": list(
            dict.fromkeys(suggestions)
        )

    }

