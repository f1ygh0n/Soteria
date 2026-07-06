"""
Central threat scoring engine.

Every scanner (Email, Website, Chat...)
uses this engine to calculate a risk score.
"""


class ThreatEngine:

    def __init__(self):

        self.score = 0
        self.findings = []

    def add_risk(self, points: int, message: str):

        self.score += points

        self.findings.append({
            "points": points,
            "message": message
        })

    def get_results(self):

        if self.score >= 80:
            level = "HIGH"

        elif self.score >= 45:
            level = "MEDIUM"

        else:
            level = "LOW"

        return {
            "risk_score": min(self.score, 100),
            "risk_level": level,
            "findings": self.findings
        }