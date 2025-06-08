from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from .agent_state import AgentState
from app.tools.cadena_suministro_tools import cadena_suministro_tools
from langgraph.graph import StateGraph, END

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

# PASO 7.4: CONSTRUCCIÓN DEL GRAFO PARA EL AGENTE DE CADENA DE SUMINISTRO

workflow_cadena_suministro = StateGraph(AgentState)

workflow_cadena_suministro.add_node("agente_cadena_suministro", agente_cadena_suministro_node)
workflow_cadena_suministro.add_node("ejecutor_herramientas_cadena", cadena_suministro_tool_node) # Nombre de nodo único

workflow_cadena_suministro.set_entry_point("agente_cadena_suministro")

def deberia_llamar_herramientas_cadena(state: AgentState) -> str: # Nombre de función único
    """
    Decide si el último mensaje del LLM (agente_cadena_suministro) contiene una llamada a herramienta.
    """
    print("--- CONDICIÓN: ¿LLAMAR HERRAMIENTA (CADENA SUMINISTRO)? ---")
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"Decisión: SÍ, llamar herramienta. Llamadas: {last_message.tool_calls}")
        return "ejecutor_herramientas_cadena"
    print("Decisión: NO, finalizar/responder.")
    return END

workflow_cadena_suministro.add_conditional_edges(
    "agente_cadena_suministro",
    deberia_llamar_herramientas_cadena,
    {
        "ejecutor_herramientas_cadena": "ejecutor_herramientas_cadena",
        END: END
    }
)

workflow_cadena_suministro.add_edge("ejecutor_herramientas_cadena", "agente_cadena_suministro")

app_cadena_suministro = workflow_cadena_suministro.compile()
print("Grafo para el Agente de Optimización de la Cadena de Suministro compilado.")
import os
try:
  graph_image_bytes = app_cadena_suministro.get_graph().draw_mermaid_png()
  image_path = os.path.join(os.path.dirname("app/assets/graphs/"), "cadena_suministro.png")
  with open(image_path, "wb") as f:
    f.write(graph_image_bytes)
    print(f"INFO: Imagen del grafo de flujo de trabajo guardada en: {image_path}")
except Exception as e:
  print(f"ADVERTENCIA: No se pudo generar la imagen del grafo de flujo de trabajo: {e}")