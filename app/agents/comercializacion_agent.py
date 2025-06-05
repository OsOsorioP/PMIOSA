from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from .agent_state import AgentState
from app.tools.comercializacion_tools import comercializacion_tools
from langgraph.graph import StateGraph, END

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

# PASO 8.4: CONSTRUCCIÓN DEL GRAFO PARA EL AGENTE DE COMERCIALIZACIÓN

workflow_comercializacion = StateGraph(AgentState)

workflow_comercializacion.add_node("agente_comercializacion", agente_comercializacion_node)
workflow_comercializacion.add_node("ejecutor_herramientas_comercializacion", comercializacion_tool_node)

workflow_comercializacion.set_entry_point("agente_comercializacion")

def deberia_llamar_herramientas_comercializacion(state: AgentState) -> str:
    """
    Decide si el último mensaje del LLM (agente_comercializacion) contiene una llamada a herramienta.
    """
    print("--- CONDICIÓN: ¿LLAMAR HERRAMIENTA (COMERCIALIZACIÓN)? ---")
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"Decisión: SÍ, llamar herramienta. Llamadas: {last_message.tool_calls}")
        return "ejecutor_herramientas_comercializacion"
    print("Decisión: NO, finalizar/responder.")
    return END

workflow_comercializacion.add_conditional_edges(
    "agente_comercializacion",
    deberia_llamar_herramientas_comercializacion,
    {
        "ejecutor_herramientas_comercializacion": "ejecutor_herramientas_comercializacion",
        END: END
    }
)

workflow_comercializacion.add_edge("ejecutor_herramientas_comercializacion", "agente_comercializacion")

app_comercializacion = workflow_comercializacion.compile()
print("Grafo para el Agente de Intermediación y Comercialización compilado.")