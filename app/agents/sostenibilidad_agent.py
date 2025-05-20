from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from agent_state import AgentState
from tools.sostenibilidad_tools import sostenibilidad_tools

agente_sostenibilidad_descripcion = """
Eres el Agente de Sostenibilidad y Prácticas Agrícolas.
Tu función es promover prácticas agrícolas sostenibles.
Utilizas análisis ambiental, modelos de sostenibilidad y bases de conocimiento (simulados por search_sustainable_practices, assess_practice_impact)
para ofrecer recomendaciones de prácticas sostenibles, reducción de emisiones y conservación de suelos.

Cuando recibas una consulta, analiza si necesitas usar alguna de tus herramientas para obtener información.
Si decides usar una herramienta, indica cuál y con qué parámetros.
Si tienes suficiente información o la herramienta ha devuelto un resultado, proporciona una respuesta concisa y útil.
"""
llm_with_sostenibilidad_tools = llm.bind_tools(sostenibilidad_tools)

sostenibilidad_tool_node = ToolNode(sostenibilidad_tools)

def agente_sostenibilidad_node(state: AgentState):
    """
    Nodo del agente de sostenibilidad. Invoca al LLM con las herramientas de sostenibilidad
    y decide la siguiente acción.
    """
    print("--- AGENTE SOSTENIBILIDAD NODE ---")
    messages = state['messages']
    response = llm_with_sostenibilidad_tools.invoke(messages)
    print(f"Respuesta del LLM (Agente Sostenibilidad): {response}")
    return {"messages": [response]}