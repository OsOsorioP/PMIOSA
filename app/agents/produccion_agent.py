from langgraph.prebuilt import ToolNode
from app.core.llm_setup import llm 
from .agent_state import AgentState
from app.tools.produccion_tools import produccion_tools
from langgraph.graph import StateGraph, END


agente_produccion_descripcion = """
Eres el Agente de Optimización de la Producción.
Tu función es proporcionar recomendaciones para maximizar la producción agrícola.
Utilizas modelos de machine learning (simulados por predict_yield, predict_optimal_harvest_window),
análisis de datos históricos y bases de conocimiento agrícola (simulados por get_crop_health_index, recommend_fertilizer_application)
para dar sugerencias de cultivos, prácticas de manejo de cultivos y optimización del uso de recursos.

Cuando recibas una consulta, analiza si necesitas usar alguna de tus herramientas para obtener información.
Si decides usar una herramienta, indica cuál y con qué parámetros.
Si tienes suficiente información o la herramienta ha devuelto un resultado, proporciona una respuesta concisa y útil.
"""

llm_with_produccion_tools = llm.bind_tools(produccion_tools)

produccion_tool_node = ToolNode(produccion_tools)

def agente_produccion_node(state: AgentState):
    """
    Nodo del agente de optimización de la producción. Invoca al LLM con las herramientas de producción
    y decide la siguiente acción (llamar a una herramienta o responder).
    """
    print("--- AGENTE PRODUCCIÓN NODE ---")
    messages = state['messages']
    # El LLM ya tiene las herramientas vinculadas.
    response = llm_with_produccion_tools.invoke(messages)
    print(f"Respuesta del LLM (Agente Producción): {response}")
    return {"messages": [response]}

# PASO 4.4: CONSTRUCCIÓN DEL GRAFO PARA EL AGENTE DE OPTIMIZACIÓN DE LA PRODUCCIÓN

workflow_produccion = StateGraph(AgentState) # Reutilizamos la misma definición de AgentState

# Añadimos los nodos
workflow_produccion.add_node("agente_produccion", agente_produccion_node)
workflow_produccion.add_node("ejecutor_herramientas_produccion", produccion_tool_node)

# Punto de entrada
workflow_produccion.set_entry_point("agente_produccion")

# Función condicional (podemos reutilizar la lógica, pero es mejor nombrarla específicamente
# por claridad, aunque su contenido sea el mismo que la de monitoreo).
def deberia_llamar_herramientas_produccion(state: AgentState) -> str:
    """
    Decide si el último mensaje del LLM (agente_produccion) contiene una llamada a herramienta.
    """
    print("--- CONDICIÓN: ¿LLAMAR HERRAMIENTA (PRODUCCIÓN)? ---")
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"Decisión: SÍ, llamar herramienta. Llamadas: {last_message.tool_calls}")
        return "ejecutor_herramientas_produccion"
    print("Decisión: NO, finalizar/responder.")
    return END

# Bordes condicionales
workflow_produccion.add_conditional_edges(
    "agente_produccion",
    deberia_llamar_herramientas_produccion,
    {
        "ejecutor_herramientas_produccion": "ejecutor_herramientas_produccion",
        END: END
    }
)

# Borde de vuelta desde el ejecutor de herramientas al agente
workflow_produccion.add_edge("ejecutor_herramientas_produccion", "agente_produccion")

# Compilamos el grafo
app_produccion = workflow_produccion.compile() # checkpointer=checkpointer si se usa

print("Grafo para el Agente de Optimización de la Producción compilado.")

# (Opcional) Visualizar el grafo
# try:
#     from IPython.display import Image, display
#     display(Image(app_produccion.get_graph().draw_png()))
#     print("Grafo de Producción visualizado.")
# except Exception as e:
#     print(f"No se pudo visualizar el grafo de Producción: {e}")