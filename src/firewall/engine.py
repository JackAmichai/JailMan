class RiskAssessment:
    def __init__(self, score: float, reason: str):
        self.score = score
        self.reason = reason

class CognitiveFirewall:
    async def analyze(self, prompt: str, history: list) -> RiskAssessment:
        # Mock implementation
        # If prompt contains "dangerous", return high risk
        if "dangerous" in prompt.lower():
            return RiskAssessment(score=0.9, reason="Dangerous content detected")
        return RiskAssessment(score=0.0, reason="Safe")
