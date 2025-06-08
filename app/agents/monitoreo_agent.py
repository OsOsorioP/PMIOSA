from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from .agent_state import AgentState
from app.tools.monitoreo_tools import monitoreo_tools
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import os

agente_monitoreo_descripcion = """
Eres el Agente de Monitoreo y Diagnóstico de Cultivos.
Tu función es recopilar y analizar datos en tiempo real sobre el estado de los cultivos.
Utilizas imágenes satelitales (simuladas por get_vegetation_index_map), análisis de datos (simulados por check_water_stress_indicators, identify_potential_issues)
para monitorear la salud de los cultivos, detectar enfermedades y plagas, y seguir el crecimiento.
También puedes solicitar inspecciones de campo (request_field_scouting).

Cuando recibas una consulta, analiza si necesitas usar alguna de tus herramientas para obtener información.
Si decides usar una herramienta, indica cuál y con qué parámetros.
Si tienes suficiente información o la herramienta ha devuelto un resultado, proporciona una respuesta concisa y útil.

Cuando se te pida realizar una tarea, revisa cuidadosamente el historial de la conversación. Si previamente solicitaste información y el usuario ha respondido, utiliza esa información proporcionada por el usuario para intentar usar tus herramientas.**
Si aún falta información crucial después de la respuesta del usuario, puedes volver a preguntar, pero sé específico sobre lo que todavía necesitas.
Si tienes toda la información necesaria del historial o de la consulta actual, procede a usar tus herramientas.
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

# CONSTRUCCIÓN DEL GRAFO PARA EL AGENTE DE MONITOREO

workflow_monitoreo = StateGraph(AgentState)

workflow_monitoreo.add_node("agente_monitoreo", agente_monitoreo_node)
workflow_monitoreo.add_node("ejecutor_herramientas_monitoreo", monitoreo_tool_node)

workflow_monitoreo.set_entry_point("agente_monitoreo")

def deberia_llamar_herramientas_monitoreo(state: AgentState) -> str:
    """
    Decide si el último mensaje del LLM (agente_monitoreo) contiene una llamada a herramienta.
    Si es así, dirige el flujo al 'ejecutor_herramientas_monitoreo'.
    De lo contrario, finaliza el flujo (END).
    """
    print("--- CONDICIÓN: ¿LLAMAR HERRAMIENTA (MONITOREO)? ---")
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"Decisión: SÍ, llamar herramienta. Llamadas: {last_message.tool_calls}")
        return "ejecutor_herramientas_monitoreo"
    print("Decisión: NO, finalizar/responder.")
    return END

workflow_monitoreo.add_conditional_edges(
    "agente_monitoreo", 
    deberia_llamar_herramientas_monitoreo,
    {
        "ejecutor_herramientas_monitoreo": "ejecutor_herramientas_monitoreo",
        END: END                                                            
    }
)

workflow_monitoreo.add_edge("ejecutor_herramientas_monitoreo", "agente_monitoreo")

checkpointer = MemorySaver() 
app_monitoreo = workflow_monitoreo.compile() 

print("Grafo para el Agente de Monitoreo compilado.")

try:
  graph_image_bytes = app_monitoreo.get_graph().draw_mermaid_png()
  image_path = os.path.join(os.path.dirname("app/assets/graphs/"), "Monitoreo.png")
  with open(image_path, "wb") as f:
    f.write(graph_image_bytes)
    print(f"INFO: Imagen del grafo de flujo de trabajo guardada en: {image_path}")
except Exception as e:
  print(f"ADVERTENCIA: No se pudo generar la imagen del grafo de flujo de trabajo: {e}")