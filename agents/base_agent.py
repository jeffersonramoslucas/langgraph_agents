
from typing import TypedDict

class AgentState(TypedDict):
    input: str
    prompt: str
    resposta: str


class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def process(self, state: AgentState) -> AgentState:
        raise NotImplementedError("Implement in subclass")
