from agents.base import BaseAgent

class CleaningAgent(BaseAgent):
    def decide(self, data):
        missing = any(row["age"] == 0 for row in data)

        decision = {
            "use_advanced_clean": missing,
            "reason": "Missing values detected" if missing else "Data looks clean"
        }

        self.log(decision["reason"])
        return decision