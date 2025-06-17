from agents.base_agent import BaseAgent, AgentState

class AgentePython(BaseAgent):
    def __init__(self, name, llm):
        super().__init__(name)
        self.llm = llm

    def process(self, state: AgentState) -> AgentState:
        prompt = f"""Você é um professor de Python. Responda de forma clara e objetiva a seguinte dúvida:

        Dúvida: {state['input']}
        """
        resposta = self.llm.invoke(prompt).content.strip()
        state["resposta"] = resposta
        return state
