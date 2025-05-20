from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from agent_state import AgentState
from tools.monitoreo_tools import monitoreo_tools

agente_monitoreo_descripcion = """
Eres el Agente de Monitoreo y Diagnóstico de Cultivos.
Tu función es recopilar y analizar datos en tiempo real sobre el estado de los cultivos.
Utilizas imágenes satelitales (simuladas por get_vegetation_index_map), análisis de datos (simulados por check_water_stress_indicators, identify_potential_issues)
para monitorear la salud de los cultivos, detectar enfermedades y plagas, y seguir el crecimiento.
También puedes solicitar inspecciones de campo (request_field_scouting).

Cuando recibas una consulta, analiza si necesitas usar alguna de tus herramientas para obtener información.
Si decides usar una herramienta, indica cuál y con qué parámetros.
Si tienes suficiente información o la herramienta ha devuelto un resultado, proporciona una respuesta concisa y útil.
"""

llm_with_monitoreo_tools = llm.bind_tools(monitoreo_tools)

monitoreo_tool_node = ToolNode(monitoreo_tools)

def agente_monitoreo_node(AgentState: dict):
    """
    Nodo del agente de monitoreo. Invoca al LLM con las herramientas de monitoreo
    y decide la siguiente acción (llamar a una herramienta o responder).
    """
    print("--- AGENTE MONITOREO NODE ---")
    messages = AgentState['messages']

    response = llm_with_monitoreo_tools.invoke(messages)
    print(f"Respuesta del LLM (Agente Monitoreo): {response}")

    return {"messages": [response]}