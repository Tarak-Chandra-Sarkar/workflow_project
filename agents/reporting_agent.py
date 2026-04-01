from agents.base import BaseAgent

class ReportingAgent(BaseAgent):

    def decide(self, data):
        if len(data) > 2:
            decision = {
                "action": "executive",
                "reason": "Large dataset",
                "confidence": 0.85
            }
        else:
            decision = {
                "action": "summary",
                "reason": "Small dataset",
                "confidence": 0.7
            }

        self.log(decision["reason"])
        return decision