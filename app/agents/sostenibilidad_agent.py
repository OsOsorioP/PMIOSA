from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from .agent_state import AgentState
from app.tools.sostenibilidad_tools import sostenibilidad_tools
from langgraph.graph import StateGraph, END

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

# PASO 6.4: CONSTRUCCIÓN DEL GRAFO PARA EL AGENTE DE SOSTENIBILIDAD

workflow_sostenibilidad = StateGraph(AgentState)

workflow_sostenibilidad.add_node("agente_sostenibilidad", agente_sostenibilidad_node)
workflow_sostenibilidad.add_node("ejecutor_herramientas_sostenibilidad", sostenibilidad_tool_node)

workflow_sostenibilidad.set_entry_point("agente_sostenibilidad")

def deberia_llamar_herramientas_sostenibilidad(state: AgentState) -> str:
    """
    Decide si el último mensaje del LLM (agente_sostenibilidad) contiene una llamada a herramienta.
    """
    print("--- CONDICIÓN: ¿LLAMAR HERRAMIENTA (SOSTENIBILIDAD)? ---")
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"Decisión: SÍ, llamar herramienta. Llamadas: {last_message.tool_calls}")
        return "ejecutor_herramientas_sostenibilidad"
    print("Decisión: NO, finalizar/responder.")
    return END

workflow_sostenibilidad.add_conditional_edges(
    "agente_sostenibilidad",
    deberia_llamar_herramientas_sostenibilidad,
    {
        "ejecutor_herramientas_sostenibilidad": "ejecutor_herramientas_sostenibilidad",
        END: END
    }
)

workflow_sostenibilidad.add_edge("ejecutor_herramientas_sostenibilidad", "agente_sostenibilidad")

app_sostenibilidad = workflow_sostenibilidad.compile()
print("Grafo para el Agente de Sostenibilidad y Prácticas Agrícolas compilado.")

import os
try:
  graph_image_bytes = app_sostenibilidad.get_graph().draw_mermaid_png()
  image_path = os.path.join(os.path.dirname("app/assets/graphs/"), "sostenibilidad.png")
  with open(image_path, "wb") as f:
    f.write(graph_image_bytes)
    print(f"INFO: Imagen del grafo de flujo de trabajo guardada en: {image_path}")
except Exception as e:
  print(f"ADVERTENCIA: No se pudo generar la imagen del grafo de flujo de trabajo: {e}")