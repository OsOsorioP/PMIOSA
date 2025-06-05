from langgraph.graph import END
from .orquestador_state import OrchestratorState, agent_node_names, agent_apps
from langchain_core.messages import AIMessage

def agent_invoker_node_revised(state: OrchestratorState, agent_app, agent_name_log: str):
    """
    Invoca el grafo de un agente específico y actualiza el estado global.
    Luego, devuelve el control al supervisor.
    """
    print(f"--- INVOCANDO AGENTE: {agent_name_log} ---")
    # La entrada para el sub-grafo del agente son los mensajes acumulados hasta ahora.
    # El último mensaje podría ser la consulta original o una instrucción/pregunta
    # específica del supervisor (si implementamos 'task_for_next_agent' en SupervisorDecision).
    # Por ahora, el sub-grafo del agente recibe todos los mensajes del estado del orquestador.
    agent_input_state = {"messages": state['messages']}

    # Invocamos el grafo del agente específico
    # El sub-grafo del agente (app_monitoreo, etc.) ya está compilado y maneja su propio
    # ciclo de herramientas si es necesario. 'invoke' ejecutará ese sub-grafo hasta su 'END'.
    agent_output_state = agent_app.invoke(agent_input_state)

    # agent_output_state['messages'] contendrá el historial del sub-grafo, incluyendo
    # la consulta que recibió, las llamadas a herramientas (si las hubo) y la respuesta final del agente.
    # Es importante que el estado del orquestador acumule estos mensajes correctamente.
    # Dado que OrchestratorState['messages'] usa operator.add, devolver la lista completa
    # de mensajes del sub-grafo debería funcionar para concatenar.
    # Sin embargo, esto podría llevar a una duplicación del historial si el sub-grafo
    # simplemente añade a los mensajes que se le pasaron.
    # Los sub-grafos de agente (app_monitoreo, etc.) fueron diseñados para tomar 'messages'
    # y devolver un estado final con 'messages' actualizados.

    # Para asegurar que solo añadimos los mensajes *generados por este agente en este turno*,
    # una estrategia más robusta sería:
    # 1. Contar cuántos mensajes había en state['messages'] *antes* de llamar al agente.
    # 2. Tomar solo los mensajes en agent_output_state['messages'] que vienen *después* de ese conteo.
    # Por simplicidad en este paso, y dado que los sub-grafos de agente terminan y devuelven
    # su estado completo, vamos a tomar todos los mensajes del agente.
    # Si el supervisor pasa el historial completo, y el agente añade a él,
    # el 'operator.add' en el estado del orquestador concatenará correctamente.

    # Lo que el agente devuelve en agent_output_state['messages'] es su historial completo
    # desde que fue invocado. Si el supervisor le pasó el historial previo, este estará incluido.
    # Para el estado del orquestador, queremos que los mensajes se acumulen.
    # La forma en que está definido OrchestratorState con operator.add se encargará de esto.
    # Devolvemos todos los mensajes que el agente procesó/generó.

    print(f"Salida del {agent_name_log} (último mensaje): {agent_output_state['messages'][-1].content if agent_output_state['messages'] and hasattr(agent_output_state['messages'][-1], 'content') else 'Agente no produjo contenido de mensaje o lista vacía'}")

    return {
        "messages": agent_output_state['messages'], # Devolvemos todos los mensajes del subgrafo del agente
        "next_agent": "supervisor" # ¡IMPORTANTE! Volver al supervisor para reevaluación.
    }

# Recreamos los nodos de agente usando la nueva función agent_invoker_node_revised
# y un nuevo nombre para el diccionario para evitar confusiones.
agent_nodes_revised = {} # Nuevo nombre para el diccionario
if 'functools' not in globals(): # Asegurar que functools está importado
    import functools

for agent_full_name, node_name_key in agent_node_names.items(): # agent_node_names y agent_apps ya están definidos
    agent_app_instance = agent_apps[node_name_key]
    agent_nodes_revised[node_name_key] = functools.partial(agent_invoker_node_revised, agent_app=agent_app_instance, agent_name_log=agent_full_name)

print("Nodos invocadores (revisados) para cada agente definidos (ahora vuelven al supervisor).")