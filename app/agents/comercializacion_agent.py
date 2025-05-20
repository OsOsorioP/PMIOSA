from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from agent_state import AgentState
from tools.comercializacion_tools import comercializacion_tools

agente_comercializacion_descripcion = """
Eres el Agente de Intermediación y Comercialización.
Tu función es actuar como intermediario entre los productores agrícolas y los usuarios finales.
Utilizas plataformas de comercio electrónico, aplicaciones móviles y sistemas de pago en línea (simulados por find_potential_buyers, verify_compliance_requirements, draft_sales_agreement, create_product_listing)
para facilitar la venta de productos agrícolas, conectar a productores con compradores y gestionar la logística de entrega.

Cuando recibas una consulta, analiza si necesitas usar alguna de tus herramientas para obtener información.
Si decides usar una herramienta, indica cuál y con qué parámetros.
Si tienes suficiente información o la herramienta ha devuelto un resultado, proporciona una respuesta concisa y útil.
"""

llm_with_comercializacion_tools = llm.bind_tools(comercializacion_tools)

comercializacion_tool_node = ToolNode(comercializacion_tools)

def agente_comercializacion_node(state: AgentState):
    """
    Nodo del agente de intermediación y comercialización. Invoca al LLM
    con las herramientas de comercialización y decide la siguiente acción.
    """
    print("--- AGENTE COMERCIALIZACIÓN NODE ---")
    messages = state['messages']
    response = llm_with_comercializacion_tools.invoke(messages)
    print(f"Respuesta del LLM (Agente Comercialización): {response}")
    return {"messages": [response]}