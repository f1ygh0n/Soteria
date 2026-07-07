from urllib.parse import urlparse
from datetime import datetime, timezone

import whois

from rapidfuzz import fuzz


POPULAR_DOMAINS = [

    "google.com",
    "gmail.com",
    "youtube.com",
    "paypal.com",
    "amazon.com",
    "apple.com",
    "microsoft.com",
    "github.com",
    "discord.com",
    "instagram.com",
    "facebook.com",
    "linkedin.com",
    "netflix.com",
    "dropbox.com",
    "openai.com",
    "x.com"

]


def get_domain(url):

    parsed = urlparse(url)

    return parsed.netloc.lower().replace("www.", "")


def get_domain_age(domain):

    try:

        info = whois.whois(domain)

        created = info.creation_date

        if isinstance(created, list):

            created = created[0]

        if not created:

            return None

        if created.tzinfo is None:

            created = created.replace(tzinfo=timezone.utc)

        age = (datetime.now(timezone.utc) - created).days

        return age

    except Exception as e:

        print("WHOIS ERROR:", e)

        return None


def detect_typosquatting(domain):

    best_match = None

    highest = 0

    for legit in POPULAR_DOMAINS:

        score = fuzz.ratio(domain, legit)

        if score > highest:

            highest = score
            best_match = legit

    if highest >= 80 and domain != best_match:

        return best_match, highest

    return None