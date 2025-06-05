from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from .agent_state import AgentState
from app.tools.monitoreo_tools import monitoreo_tools
from langgraph.graph import StateGraph, END

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

# PASO 3.6: CONSTRUCCIÓN DEL GRAFO PARA EL AGENTE DE MONITOREO

# Crearemos un nuevo grafo de estado.
workflow_monitoreo = StateGraph(AgentState)

# Añadimos los nodos al grafo:
# 1. El nodo del agente de monitoreo (que definimos como 'agente_monitoreo_node')
# 2. El nodo de ejecución de herramientas ('monitoreo_tool_node')

workflow_monitoreo.add_node("agente_monitoreo", agente_monitoreo_node)
workflow_monitoreo.add_node("ejecutor_herramientas_monitoreo", monitoreo_tool_node)

# Ahora definimos las transiciones (edges) entre los nodos.

# Establecemos el punto de entrada del grafo.
# Cuando el grafo comience, la primera llamada será al nodo "agente_monitoreo".
workflow_monitoreo.set_entry_point("agente_monitoreo")

# Después de que el "agente_monitoreo" se ejecute, necesitamos decidir a dónde ir.
# ¿Debe llamar a una herramienta o ha terminado?
# Creamos una función condicional para esto.
def deberia_llamar_herramientas_monitoreo(state: AgentState) -> str:
    """
    Decide si el último mensaje del LLM (agente_monitoreo) contiene una llamada a herramienta.
    Si es así, dirige el flujo al 'ejecutor_herramientas_monitoreo'.
    De lo contrario, finaliza el flujo (END).
    """
    print("--- CONDICIÓN: ¿LLAMAR HERRAMIENTA (MONITOREO)? ---")
    last_message = state['messages'][-1]
    # Si el LLM generó tool_calls, entonces debemos ejecutar las herramientas.
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"Decisión: SÍ, llamar herramienta. Llamadas: {last_message.tool_calls}")
        return "ejecutor_herramientas_monitoreo"
    # De lo contrario, el LLM ha respondido y podemos finalizar (por ahora).
    print("Decisión: NO, finalizar/responder.")
    return END # END es una constante especial de LangGraph que indica el final del flujo.

# Añadimos el borde condicional desde "agente_monitoreo":
workflow_monitoreo.add_conditional_edges(
    "agente_monitoreo", # Nodo de origen
    deberia_llamar_herramientas_monitoreo, # Función que decide la ruta
    {
        "ejecutor_herramientas_monitoreo": "ejecutor_herramientas_monitoreo", # Si la función devuelve esto, ir a este nodo
        END: END                                                              # Si la función devuelve END, terminar
    }
)

# Después de que el "ejecutor_herramientas_monitoreo" se ejecute,
# el resultado (ToolMessage) debe volver al "agente_monitoreo" para que lo procese.
workflow_monitoreo.add_edge("ejecutor_herramientas_monitoreo", "agente_monitoreo")

# Compilamos el grafo para hacerlo ejecutable.
# También añadimos un MemorySaver para poder inspeccionar los pasos intermedios si es necesario.
# checkpointer = MemorySaver() # Descomentar si quieres persistencia en memoria para depuración.
app_monitoreo = workflow_monitoreo.compile() # checkpointer=checkpointer si se usa

print("Grafo para el Agente de Monitoreo compilado.")

# (Opcional) Visualizar el grafo (requiere graphviz)
# try:
#     from IPython.display import Image, display
#     display(Image(app_monitoreo.get_graph().draw_png()))
#     print("Grafo visualizado (si graphviz está instalado).")
# except Exception as e:
#     print(f"No se pudo visualizar el grafo (graphviz podría no estar instalado): {e}")