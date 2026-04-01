from agents.base import BaseAgent

class CleaningAgent(BaseAgent):

    def decide(self, data):
        missing = any(row["age"] == 0 for row in data)

        decision = {
            "action": "advanced_clean" if missing else "basic_clean",
            "reason": "Missing values detected" if missing else "Data looks clean",
            "confidence": 0.9 if missing else 0.7
        }

        self.log(decision["reason"])
        return decision