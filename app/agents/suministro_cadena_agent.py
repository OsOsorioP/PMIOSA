from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from agent_state import AgentState
from tools.cadena_suministro_tools import cadena_suministro_tools

agente_cadena_descripcion = """
Eres el Agente de Optimización de la Cadena de Suministro.
Tu función es optimizar la cadena de suministro agrícola desde la producción hasta la entrega al usuario final.
Utilizas modelos de optimización, sistemas de gestión de inventarios y plataformas de logística (simulados por get_market_price_data, get_transport_options, get_storage_availability, simulate_sales_scenario)
para la gestión eficiente de inventarios, optimización de rutas de transporte y reducción de desperdicios.

Cuando recibas una consulta, analiza si necesitas usar alguna de tus herramientas para obtener información.
Si decides usar una herramienta, indica cuál y con qué parámetros.
Si tienes suficiente información o la herramienta ha devuelto un resultado, proporciona una respuesta concisa y útil.
"""

llm_with_cadena_suministro_tools = llm.bind_tools(cadena_suministro_tools)

cadena_suministro_tool_node = ToolNode(cadena_suministro_tools)

def agente_cadena_suministro_node(state: AgentState):
    """
    Nodo del agente de optimización de la cadena de suministro. Invoca al LLM
    con las herramientas de cadena de suministro y decide la siguiente acción.
    """
    print("--- AGENTE CADENA DE SUMINISTRO NODE ---")
    messages = state['messages']
    response = llm_with_cadena_suministro_tools.invoke(messages)
    print(f"Respuesta del LLM (Agente Cadena Suministro): {response}")
    return {"messages": [response]}