from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from .agent_state import AgentState
from app.tools.gestion_riesgos_tools import gestion_riesgos_tools
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage,BaseMessage

agente_riesgos_descripcion = """
Eres el Agente de Predicción y Mitigación de Riesgos.
Tu función es identificar y mitigar riesgos relacionados con la producción agrícola y la cadena de suministro.
Utilizas modelos de análisis de riesgos, sistemas de alerta temprana y planes de contingencia (simulados por predict_extreme_weather_event, assess_pest_disease_outbreak_risk, forecast_market_price_volatility, recommend_risk_mitigation_strategy)
para la prevención de pérdidas de cosechas, manejo de riesgos climáticos y respuesta a interrupciones en la cadena de suministro.

Cuando recibas una consulta, analiza si necesitas usar alguna de tus herramientas para obtener información.
Si decides usar una herramienta, indica cuál y con qué parámetros.
Si tienes suficiente información o la herramienta ha devuelto un resultado, proporciona una respuesta concisa y útil.
"""

llm_with_gestion_riesgos_tools = llm.bind_tools(gestion_riesgos_tools)

gestion_riesgos_tool_node = ToolNode(gestion_riesgos_tools)

def agente_gestion_riesgos_node(state: AgentState):
    print("--- AGENTE GESTIÓN RIESGOS NODE ---")
    
    messages_for_llm: list[BaseMessage] = []

    messages_for_llm.append(SystemMessage(content=agente_riesgos_descripcion))
    messages_for_llm.extend(state['messages'])

    response = llm_with_gestion_riesgos_tools.invoke(messages_for_llm)
    print(f"Respuesta del LLM (Agente Gestión Riesgos): {response.content if hasattr(response, 'content') else response}")
    
    return {"messages": [response]}

# PASO 9.4: CONSTRUCCIÓN DEL GRAFO PARA EL AGENTE DE GESTIÓN DE RIESGOS

workflow_gestion_riesgos = StateGraph(AgentState)

workflow_gestion_riesgos.add_node("agente_gestion_riesgos", agente_gestion_riesgos_node)
workflow_gestion_riesgos.add_node("ejecutor_herramientas_riesgos", gestion_riesgos_tool_node) # Nombre de nodo único

workflow_gestion_riesgos.set_entry_point("agente_gestion_riesgos")

def deberia_llamar_herramientas_riesgos(state: AgentState) -> str: # Nombre de función único
    """
    Decide si el último mensaje del LLM (agente_gestion_riesgos) contiene una llamada a herramienta.
    """
    print("--- CONDICIÓN: ¿LLAMAR HERRAMIENTA (GESTIÓN RIESGOS)? ---")
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"Decisión: SÍ, llamar herramienta. Llamadas: {last_message.tool_calls}")
        return "ejecutor_herramientas_riesgos"
    print("Decisión: NO, finalizar/responder.")
    return END

workflow_gestion_riesgos.add_conditional_edges(
    "agente_gestion_riesgos",
    deberia_llamar_herramientas_riesgos,
    {
        "ejecutor_herramientas_riesgos": "ejecutor_herramientas_riesgos",
        END: END
    }
)

workflow_gestion_riesgos.add_edge("ejecutor_herramientas_riesgos", "agente_gestion_riesgos")

app_gestion_riesgos = workflow_gestion_riesgos.compile()
print("Grafo para el Agente de Predicción y Mitigación de Riesgos compilado.")

import os
try:
  graph_image_bytes = app_gestion_riesgos.get_graph().draw_mermaid_png()
  image_path = os.path.join(os.path.dirname("app/assets/graphs/"), "gestion_riesgos.png")
  with open(image_path, "wb") as f:
    f.write(graph_image_bytes)
    print(f"INFO: Imagen del grafo de flujo de trabajo guardada en: {image_path}")
except Exception as e:
  print(f"ADVERTENCIA: No se pudo generar la imagen del grafo de flujo de trabajo: {e}")