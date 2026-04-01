from agents.base import BaseAgent

class TransformationAgent(BaseAgent):

    def decide(self, data):
        countries = set(row["country"] for row in data)

        if len(countries) > 1:
            decision = {
                "action": "advanced",
                "reason": "Multiple countries detected",
                "confidence": 0.9
            }
        else:
            decision = {
                "action": "basic",
                "reason": "Single country dataset",
                "confidence": 0.7
            }

        self.log(decision["reason"])
        return decision