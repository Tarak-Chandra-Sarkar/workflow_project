class BaseAgent:
    def __init__(self, name):
        self.name = name

    def decide(self, context):
        raise NotImplementedError

    def log(self, message):
        print(f"[{self.name}] {message}")