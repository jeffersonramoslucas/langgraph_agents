import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda



from agents.base_agent import AgentState
from agents.agente_avaliador import AgenteAvaliador
from agents.agente_python import AgentePython
from agents.agente_analise_dados import AgenteAnaliseDados
from orchestrator.router import AgentRouter

llm = ChatOpenAI(model="gpt-4", temperature=0.0)

agent_router = AgentRouter("orquestrador", llm)
agent_python = AgentePython("professor_python", llm)
agent_dados = AgenteAnaliseDados("professor_analise_dados", llm)
agent_avaliador = AgenteAvaliador("avaliador", llm)

workflow = StateGraph(AgentState)

workflow.add_node("orquestrador", RunnableLambda(agent_router.process))
workflow.add_node("professor_python", RunnableLambda(agent_python.process))
workflow.add_node("professor_dados", RunnableLambda(agent_dados.process))
workflow.add_node("avaliador_final", RunnableLambda(agent_avaliador.process))
workflow.add_node("fallback", RunnableLambda(agent_router.fallback))

workflow.set_entry_point("orquestrador")

workflow.add_conditional_edges(
    "orquestrador",
    lambda state: state["next"],
    {
        "professor_python": "professor_python",
        "professor_dados": "professor_dados",
        "fallback": "fallback"
    }
)

workflow.add_edge("professor_python", "avaliador_final")
workflow.add_edge("professor_dados", "avaliador_final")
workflow.add_edge("fallback", "avaliador_final")
workflow.add_edge("avaliador_final", END)

graph = workflow.compile()

graph.invoke({"input": "Como faço um loop for em Python?"})
graph.invoke({"input": "Qual a diferença entre uma lista e uma tupla em Python?"})
graph.invoke({"input": "Qual a diferença entre regressão linear e logística?"})
graph.invoke({"input": "Como lidar com dados ausentes em um DataFrame?"})
graph.invoke({"input": "Qual a capital da França?"})
graph.invoke({"input": "Como funciona um motor a combustão?"})
