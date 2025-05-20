from orquestador_state import OrchestratorState
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from invoker import supervisor_node_iterative, agent_nodes_revised
from orquestador_agent import agent_node_names

def error_handler_node(state: OrchestratorState):
    print("--- ERROR HANDLER NODE ---")
    # Podríamos implementar lógica más sofisticada aquí, como pedir al usuario que reintente o clarifique.
    # Por ahora, simplemente finaliza.
    error_message = "Lo siento, he encontrado un problema y no puedo procesar tu solicitud en este momento."
    if state['messages'] and hasattr(state['messages'][-1], 'content') and "Supervisor: Error" in state['messages'][-1].content:
        error_message = state['messages'][-1].content # Usa el mensaje de error del supervisor si existe
    return {"messages": [AIMessage(content=error_message)], "next_agent": END}

orchestrator_workflow_iterative = StateGraph(OrchestratorState)

# Añadir el nodo supervisor (usando la nueva función 'supervisor_node_iterative' del Paso B)
orchestrator_workflow_iterative.add_node("supervisor", supervisor_node_iterative)

# Añadir los nodos invocadores de agentes (usando 'agent_nodes_revised' del Paso C)
for node_name, node_function in agent_nodes_revised.items():
    orchestrator_workflow_iterative.add_node(node_name, node_function)

# El nodo error_handler sigue siendo útil (definido en tu Paso 10.4 original)
# Asegúrate de que 'error_handler_node' esté definido antes de esta línea.
orchestrator_workflow_iterative.add_node("error_handler", error_handler_node)

# Establecer el punto de entrada
orchestrator_workflow_iterative.set_entry_point("supervisor")

# Nueva función de enrutamiento desde el supervisor
def route_from_supervisor_iterative(state: OrchestratorState) -> str:
    """
    Decide el siguiente nodo basado en el campo 'next_agent' establecido por el supervisor_node_iterative.
    Puede ser el nombre de un nodo de agente, END, o 'error_handler'.
    """
    print(f"--- RUTA DESDE SUPERVISOR (ITERATIVO) --- Próximo destino: {state.get('next_agent')}")
    next_node_decision = state.get("next_agent")

    if next_node_decision == END:
        return END # El supervisor decidió finalizar y responder al usuario.
    elif next_node_decision in agent_node_names.values(): # agent_node_names.values() son los nombres cortos como "monitoreo_cultivos"
        return next_node_decision # Ir al agente especificado
    elif next_node_decision == "error_handler":
        return "error_handler"
    else:
        # Caso inesperado, podría ser un error en la lógica del supervisor
        print(f"Advertencia: Decisión de enrutamiento inesperada desde el supervisor: {next_node_decision}. Dirigiendo a error_handler.")
        return "error_handler"

# Mapa de rutas condicionales desde el supervisor.
# Incluye todos los agentes, END, y error_handler.
conditional_map_supervisor = {node_name: node_name for node_name in agent_node_names.values()}
conditional_map_supervisor[END] = END # Si 'next_agent' es END, el flujo termina.
conditional_map_supervisor["error_handler"] = "error_handler"

orchestrator_workflow_iterative.add_conditional_edges(
    "supervisor",                   # Nodo de origen
    route_from_supervisor_iterative, # Función que devuelve el nombre del siguiente nodo
    conditional_map_supervisor      # Mapa de posibles siguientes nodos
)

# ¡IMPORTANTE! Bordes desde cada nodo de agente DE VUELTA al nodo "supervisor".
# La función 'agent_invoker_node_revised' (del Paso C) ya establece state['next_agent'] = "supervisor",
# pero la arista física en el grafo debe existir.
for agent_node_key in agent_node_names.values(): # Itera sobre los nombres de nodo cortos (ej. "monitoreo_cultivos")
    orchestrator_workflow_iterative.add_edge(agent_node_key, "supervisor")

# Borde desde 'error_handler' a END (esto se mantiene igual)
orchestrator_workflow_iterative.add_edge("error_handler", END)

# Compilar el nuevo grafo del orquestador
# Si usas checkpointer:
# from langgraph.checkpoint.memory import MemorySaver
# checkpointer_orchestrator_iterative = MemorySaver()
# app_orchestrator_iterative = orchestrator_workflow_iterative.compile(checkpointer=checkpointer_orchestrator_iterative)

# Sin checkpointer:
app_orchestrator_iterative = orchestrator_workflow_iterative.compile()

print("Grafo del Orquestador Iterativo compilado.")

# (Opcional) Visualizar el nuevo grafo (usando el código del Paso 10.6.1 o 10.6.2,
# pero aplicado a 'app_orchestrator_iterative')
# Ejemplo con Mermaid:
if 'app_orchestrator_iterative' in globals():
    try:
        mermaid_code_iterative = app_orchestrator_iterative.get_graph().draw_mermaid()
        print("\n--- Código Mermaid del Grafo del Orquestador Iterativo ---")
        print(mermaid_code_iterative)
        print("----------------------------------------------------------")
    except Exception as e:
        print(f"No se pudo generar el código Mermaid para el grafo iterativo: {e}")