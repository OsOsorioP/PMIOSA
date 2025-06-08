from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from .agent_state import AgentState
from app.tools.hidricos_tools import hidricos_tools
from langgraph.graph import StateGraph, END

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

# PASO 5.4: CONSTRUCCIÓN DEL GRAFO PARA EL AGENTE DE GESTIÓN DE RECURSOS HÍDRICOS

workflow_hidrico = StateGraph(AgentState)

workflow_hidrico.add_node("agente_hidrico", agente_hidrico_node)
workflow_hidrico.add_node("ejecutor_herramientas_hidrico", hidricos_tool_node)

workflow_hidrico.set_entry_point("agente_hidrico")

def deberia_llamar_herramientas_hidrico(state: AgentState) -> str:
    """
    Decide si el último mensaje del LLM (agente_hidrico) contiene una llamada a herramienta.
    """
    print("--- CONDICIÓN: ¿LLAMAR HERRAMIENTA (HÍDRICO)? ---")
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"Decisión: SÍ, llamar herramienta. Llamadas: {last_message.tool_calls}")
        return "ejecutor_herramientas_hidrico"
    print("Decisión: NO, finalizar/responder.")
    return END

workflow_hidrico.add_conditional_edges(
    "agente_hidrico",
    deberia_llamar_herramientas_hidrico,
    {
        "ejecutor_herramientas_hidrico": "ejecutor_herramientas_hidrico",
        END: END
    }
)

workflow_hidrico.add_edge("ejecutor_herramientas_hidrico", "agente_hidrico")

app_hidrico = workflow_hidrico.compile()
print("Grafo para el Agente de Gestión de Recursos Hídricos compilado.")

import os
try:
  graph_image_bytes = app_hidrico.get_graph().draw_mermaid_png()
  image_path = os.path.join(os.path.dirname("app/assets/graphs/"), "hidrico.png")
  with open(image_path, "wb") as f:
    f.write(graph_image_bytes)
    print(f"INFO: Imagen del grafo de flujo de trabajo guardada en: {image_path}")
except Exception as e:
  print(f"ADVERTENCIA: No se pudo generar la imagen del grafo de flujo de trabajo: {e}")