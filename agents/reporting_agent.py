from agents.base import BaseAgent

class ReportingAgent(BaseAgent):
    def decide(self, data):
        if len(data) > 2:
            decision = {
                "style": "executive",
                "reason": "Large dataset"
            }
        else:
            decision = {
                "style": "summary",
                "reason": "Small dataset"
            }

        self.log(decision["reason"])
        return decision