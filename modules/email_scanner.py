import re

from modules.threat_engine import ThreatEngine
from utils.constants import (
    URGENCY_WORDS,
    CREDENTIAL_WORDS,
    FINANCIAL_WORDS,
    IMPERSONATION_TARGETS
)


class EmailScanner:

    def __init__(self):

        self.engine = ThreatEngine()

    def scan(self, email_text: str):

        self.engine = ThreatEngine()

        text = email_text.lower()

        self.check_keywords(text)
        self.check_links(text)

        return self.engine.get_results()

    def check_keywords(self, text):

        for word in URGENCY_WORDS:

            if word in text:

                self.engine.add_risk(
                    12,
                    f'Urgency detected: "{word}"'
                )

        for word in CREDENTIAL_WORDS:

            if word in text:

                self.engine.add_risk(
                    18,
                    f'Credential request: "{word}"'
                )

        for word in FINANCIAL_WORDS:

            if word in text:

                self.engine.add_risk(
                    10,
                    f'Financial keyword: "{word}"'
                )

        for company in IMPERSONATION_TARGETS:

            if company in text:

                self.engine.add_risk(
                    15,
                    f'Possible impersonation of {company.title()}'
                )

    def check_links(self, text):

        urls = re.findall(
            r'https?://\S+',
            text
        )

        if len(urls) > 0:

            self.engine.add_risk(
                20,
                f"{len(urls)} URL(s) detected"
            )