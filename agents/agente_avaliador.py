from agents.base_agent import BaseAgent, AgentState

class AgenteAvaliador(BaseAgent):
    def __init__(self, name, llm):
        super().__init__(name)
        self.llm = llm

    def process(self, state: AgentState) -> AgentState:
        print("\n📘 Resposta final:")
        print(state["resposta"])
        return state
