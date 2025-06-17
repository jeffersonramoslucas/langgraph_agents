from agents.base_agent import AgentState, BaseAgent

class AgentRouter(BaseAgent):
    def __init__(self, name, llm):
        super().__init__(name)
        self.llm = llm

    def process(self, state: AgentState) -> AgentState:
        prompt = f"""Classifique a pergunta como 'python', 'dados' ou 'outro'. Responda apenas com uma palavra.

        Pergunta: {state['input']}
        """
        topico = self.llm.invoke(prompt).content.strip().lower()
        topico = topico.replace(".", "").replace("'", "").strip()
        print(f"🔀 Classificação: {topico}")

        state["topico"] = topico

        if "dados" in topico:
            state["next"] = "professor_dados"
        elif "python" in topico:
            state["next"] = "professor_python"
        else:
            state["next"] = "fallback"

        return state
    
    def fallback(self, state: AgentState) -> AgentState:
        state["resposta"] = "Nenhum especialista disponível para esse tipo de pergunta."
        return state
