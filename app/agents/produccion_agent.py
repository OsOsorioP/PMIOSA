from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from agent_state import AgentState
from tools.produccion_tools import produccion_tools


agente_produccion_descripcion = """
Eres el Agente de Optimización de la Producción.
Tu función es proporcionar recomendaciones para maximizar la producción agrícola.
Utilizas modelos de machine learning (simulados por predict_yield, predict_optimal_harvest_window),
análisis de datos históricos y bases de conocimiento agrícola (simulados por get_crop_health_index, recommend_fertilizer_application)
para dar sugerencias de cultivos, prácticas de manejo de cultivos y optimización del uso de recursos.

Cuando recibas una consulta, analiza si necesitas usar alguna de tus herramientas para obtener información.
Si decides usar una herramienta, indica cuál y con qué parámetros.
Si tienes suficiente información o la herramienta ha devuelto un resultado, proporciona una respuesta concisa y útil.
"""

llm_with_produccion_tools = llm.bind_tools(produccion_tools)

produccion_tool_node = ToolNode(produccion_tools)

def agente_produccion_node(state: AgentState):
    """
    Nodo del agente de optimización de la producción. Invoca al LLM con las herramientas de producción
    y decide la siguiente acción (llamar a una herramienta o responder).
    """
    print("--- AGENTE PRODUCCIÓN NODE ---")
    messages = state['messages']
    # El LLM ya tiene las herramientas vinculadas.
    response = llm_with_produccion_tools.invoke(messages)
    print(f"Respuesta del LLM (Agente Producción): {response}")
    return {"messages": [response]}