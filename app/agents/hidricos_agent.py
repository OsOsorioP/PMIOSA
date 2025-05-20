from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from agent_state import AgentState
from tools.hidricos_tools import hidricos_tools

agente_hidrico_descripcion = """
Eres el Agente de Gestión de Recursos Hídricos.
Tu función es optimizar el uso del agua en la agricultura.
Utilizas datos de estaciones meteorológicas (simulados por get_weather_forecast),
sensores de humedad del suelo (simulados por get_soil_moisture) y modelos de optimización
para la planificación de riego, monitoreo de la calidad del agua (simulado por get_water_quality) y prevención de escasez.

Cuando recibas una consulta, analiza si necesitas usar alguna de tus herramientas para obtener información.
Si decides usar una herramienta, indica cuál y con qué parámetros.
Si tienes suficiente información o la herramienta ha devuelto un resultado, proporciona una respuesta concisa y útil.
"""

llm_with_hidricos_tools = llm.bind_tools(hidricos_tools)

hidricos_tool_node = ToolNode(hidricos_tools)

def agente_hidrico_node(state: AgentState):
    """
    Nodo del agente de gestión de recursos hídricos. Invoca al LLM con las herramientas hídricas
    y decide la siguiente acción.
    """
    print("--- AGENTE RECURSOS HÍDRICOS NODE ---")
    messages = state['messages']
    response = llm_with_hidricos_tools.invoke(messages)
    print(f"Respuesta del LLM (Agente Recursos Hídricos): {response}")
    return {"messages": [response]}