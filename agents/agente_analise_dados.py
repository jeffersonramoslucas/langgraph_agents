from agents.base_agent import BaseAgent, AgentState

class AgenteAnaliseDados(BaseAgent):
    def __init__(self, name, llm):
        super().__init__(name)
        self.llm = llm

    def process(self, state: AgentState) -> AgentState:
        prompt = f"""Você é um professor especialista em análise de dados com Python. Responda de forma didática:

        Dúvida: {state['input']}
        """
        resposta = self.llm.invoke(prompt).content.strip()
        state["resposta"] = resposta
        return state
