import secrets
import string

from utils.password_rules import analyze_password


LETTER_REPLACEMENTS = {

    "a": "@",
    "A": "@",

    "e": "3",
    "E": "3",

    "i": "1",
    "I": "1",

    "o": "0",
    "O": "0",

    "s": "$",
    "S": "$",

    "t": "7",
    "T": "7"

}

SYMBOLS = "!@#$%^&*()-_=+?"

TARGET_LENGTH = 16

MAX_ATTEMPTS = 100

def generate_secure_password(

    length=16,

    uppercase=True,

    lowercase=True,

    numbers=True,

    symbols=True

):

    if length < 8:
        raise ValueError("Password length must be at least 8.")

    pools = []

    password = []

    if uppercase:

        pools.append(string.ascii_uppercase)

        password.append(secrets.choice(string.ascii_uppercase))

    if lowercase:

        pools.append(string.ascii_lowercase)

        password.append(secrets.choice(string.ascii_lowercase))

    if numbers:

        pools.append(string.digits)

        password.append(secrets.choice(string.digits))

    if symbols:

        pools.append(SYMBOLS)

        password.append(secrets.choice(SYMBOLS))

    if not pools:
        raise ValueError("No character sets selected.")

    pool = "".join(pools)

    while len(password) < length:

        password.append(

            secrets.choice(pool)

        )

    secrets.SystemRandom().shuffle(password)

    return "".join(password)

def improve_password(password):

    chars = list(password)

    replaced = 0

    for i, char in enumerate(chars):

        if (
            char in LETTER_REPLACEMENTS
            and replaced < 3
            and secrets.randbelow(100) < 50
        ):

            chars[i] = LETTER_REPLACEMENTS[char]

            replaced += 1

    password = chars

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in SYMBOLS for c in password)

    if not has_upper:

        password.insert(

            secrets.randbelow(len(password)+1),

            secrets.choice(string.ascii_uppercase)

        )

    if not has_lower:

        password.insert(

            secrets.randbelow(len(password)+1),

            secrets.choice(string.ascii_lowercase)

        )

    if not has_digit:

        password.insert(

            secrets.randbelow(len(password)+1),

            secrets.choice(string.digits)

        )

    if not has_symbol:

        password.insert(

            secrets.randbelow(len(password)+1),

            secrets.choice(SYMBOLS)

        )

    pool = (

        string.ascii_letters +

        string.digits +

        SYMBOLS

    )

    while len(password) < TARGET_LENGTH:

        password.insert(

            secrets.randbelow(len(password)+1),

            secrets.choice(pool)

        )

    return "".join(password)

def generate_suggestions(

    password,

    count=3,

    minimum_score=80

):

    suggestions = []

    seen = set()

    attempts = 0

    while (

        len(suggestions) < count

        and attempts < MAX_ATTEMPTS

    ):

        candidate = improve_password(password)

        attempts += 1

        if candidate in seen:
            continue

        analysis = analyze_password(candidate)

        if analysis["score"] < minimum_score:
            continue

        seen.add(candidate)

        suggestions.append({

            "password": candidate,

            "score": analysis["score"],

            "strength": analysis["strength"]

        })

    return suggestions