from orquestador_state import OrchestratorState
from langgraph.graph import END

def decide_continuation_node(state: OrchestratorState):
    print("--- DECIDE CONTINUATION NODE ---")
    # Por ahora, después de que un agente responde, consideramos la tarea completada.
    # En un sistema más complejo, aquí podríamos:
    # 1. Preguntar al LLM supervisor si se necesita otro agente.
    # 2. Verificar si el usuario está satisfecho.
    # 3. Pasar a un agente de resumen o presentación.
    print("La tarea del agente ha finalizado. Terminando el flujo principal.")
    # No necesitamos cambiar 'next_agent' si queremos ir a END.
    # El borde condicional se encargará de esto.
    # Simplemente devolvemos el estado actual.
    return {"next_agent": END} # O podríamos tener un estado explícito como "finalizar_flujo"