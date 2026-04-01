from agents.base import BaseAgent

class TransformationAgent(BaseAgent):
    def decide(self, data):
        countries = set(row["country"] for row in data)

        if len(countries) > 1:
            decision = {
                "mode": "advanced",
                "reason": "Multiple countries detected"
            }
        else:
            decision = {
                "mode": "basic",
                "reason": "Single country dataset"
            }

        self.log(decision["reason"])
        return decision