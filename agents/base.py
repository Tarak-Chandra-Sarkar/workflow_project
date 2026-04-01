import logging

logging.basicConfig(level=logging.INFO)

class BaseAgent:
    def __init__(self, name):
        self.name = name

    def decide(self, context):
        raise NotImplementedError

    def log(self, message):
        logging.info(f"[{self.name}] {message}")