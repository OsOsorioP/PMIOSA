from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal, Optional
from langchain_core.messages import AIMessage
from app.core.llm_setup import llm
from .orquestador_state import OrchestratorState, agent_names, agent_node_names, agent_descriptions_map
from langgraph.graph import END


class SupervisorDecision(BaseModel):
    action: Literal["route_to_agent", "respond_to_user", "ask_user_for_clarification"] = Field(
        description="La acción a tomar. 'route_to_agent' para delegar a otro agente, 'respond_to_user' para dar la respuesta final."
    )
    next_agent_name: Optional[str] = Field( # Optional y con default None
        None, description=f"Si la acción es 'route_to_agent', el nombre del agente que debe manejar la siguiente tarea. Debe ser uno de: {', '.join(agent_names)}"
    )
    final_answer: Optional[str] = Field( # Optional y con default None
        None, description="Si la acción es 'respond_to_user', esta es la respuesta final compilada para el usuario."
    )
    question_for_user: Optional[str] = Field(
        None, description="Si la acción es 'ask_user_for_clarification', esta es la pregunta para el usuario."
    )

prompt_template_supervisor_iterative = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un supervisor experto de una plataforma agrícola multiagente. Tu objetivo es orquestar a un equipo de agentes especializados para responder completamente a la consulta del usuario. "
     "Analiza la consulta original del usuario y el historial de la conversación, incluyendo las respuestas de los agentes que ya han intervenido.\n\n"
     "Agentes Disponibles y sus funciones:\n" +
     "\n".join([f"- {name}: {agent_descriptions_map[name].splitlines()[1].strip()}" for name in agent_names]) + # Tomamos la función principal
     "\n\nProceso a seguir:\n"
     "1. Si esta es la primera interacción o la respuesta anterior de un agente no es suficiente: Decide qué agente especializado es el MÁS adecuado para el SIGUIENTE PASO. Especifica 'route_to_agent' y el 'next_agent_name'.\n"
     "2. Si consideras que la consulta original del usuario ha sido COMPLETAMENTE RESPONDIDA con la información disponible (incluyendo la última respuesta del agente): Especifica 'respond_to_user' y proporciona la 'final_answer' consolidada.\n"
     "3. Si la última respuesta de un agente es una PREGUNTA que requiere información adicional del usuario para proceder: Especifica la acción 'request_user_input' y formula la pregunta que se debe hacer al usuario final.\n"
     "Sé conciso y directo en tu decisión. No añadas explicaciones extra a menos que sea la respuesta final al usuario."
     ),
    # El historial de mensajes se pasará dinámicamente a través de la variable 'messages'.
    # La plantilla de mensajes de Langchain puede manejar una lista de mensajes.
    # Aquí, el último mensaje "human" es el que desencadena la respuesta del LLM.
    # La variable {messages} será una lista de BaseMessage objects.
    # La variable {original_query} se pasa para referencia explícita.
    ("human", "Consulta original del usuario: {original_query}\n\nHistorial de la conversación actual:\n{messages}\n\nConsiderando el historial y la consulta original, ¿cuál es el siguiente paso o la respuesta final?")
])
    
supervisor_llm = llm

supervisor_chain_iterative = prompt_template_supervisor_iterative | supervisor_llm.with_structured_output(SupervisorDecision)

def supervisor_node_iterative(state: OrchestratorState):
    print("--- SUPERVISOR NODE (ITERATIVO) ---")
    original_query = state['original_query']
    messages_for_prompt = state['messages']

    print(f"Supervisor analizando consulta original: {original_query}")
    if len(messages_for_prompt) > 1:
        print(f"Último mensaje en el historial para el supervisor: {messages_for_prompt[-1]}")

    try:
        decision: SupervisorDecision = supervisor_chain_iterative.invoke({
            "original_query": original_query,
            "messages": messages_for_prompt
        })
        print(f"Decisión del Supervisor: {decision}")

        # --- Prints de depuración (puedes mantenerlos o quitarlos después) ---
        print(f"DEBUG: decision.action = '{decision.action}'")
        if decision.action == "ask_user_for_clarification":
            print(f"DEBUG: decision.question_for_user = '{decision.question_for_user}'")
        elif decision.action == "respond_to_user":
            print(f"DEBUG: decision.final_answer = '{decision.final_answer}'")
        elif decision.action == "route_to_agent":
            print(f"DEBUG: decision.next_agent_name = '{decision.next_agent_name}'")
        # --- Fin de prints de depuración ---

        new_messages_for_state = []

        if decision.action == "ask_user_for_clarification" and decision.question_for_user:
            print("Supervisor: Acción decidida -> ask_user_for_clarification")
            new_messages_for_state.append(AIMessage(content=decision.question_for_user))
            return {
                "messages": new_messages_for_state,
                "next_agent": END
            }
        elif decision.action == "respond_to_user" and decision.final_answer:
            print("Supervisor: Acción decidida -> respond_to_user")
            new_messages_for_state.append(AIMessage(content=decision.final_answer))
            return {
                "messages": new_messages_for_state,
                "next_agent": END
            }
        elif decision.action == "route_to_agent" and decision.next_agent_name: # <--- ESTA ES LA RAMA QUE FALTABA O ESTABA MAL COLOCADA
            print(f"Supervisor: Acción decidida -> route_to_agent ({decision.next_agent_name})")
            selected_agent_full_name = decision.next_agent_name
            if selected_agent_full_name in agent_node_names:
                next_node_name = agent_node_names[selected_agent_full_name]
                routing_message_content = f"Supervisor: Entendido. Voy a consultar al {selected_agent_full_name} sobre esto."
                new_messages_for_state.append(AIMessage(content=routing_message_content))
                return {
                    "messages": new_messages_for_state,
                    "next_agent": next_node_name
                }
            else:
                print(f"Error: El agente '{selected_agent_full_name}' (nombre completo) no está en agent_node_names.")
                error_msg_content = f"Supervisor: Lo siento, no pude encontrar un agente llamado '{selected_agent_full_name}' para manejar tu solicitud."
                new_messages_for_state.append(AIMessage(content=error_msg_content))
                return {"messages": new_messages_for_state, "next_agent": "error_handler"}
        else:
            # Este 'else' se activa si la 'action' no es ninguna de las esperadas O
            # si los campos requeridos (como question_for_user, final_answer, next_agent_name) son None cuando deberían tener valor.
            print(f"Error: Decisión inválida o incompleta del supervisor: {decision}. La acción fue '{decision.action}' pero los campos requeridos podrían faltar.")
            error_msg_content = "Supervisor: Hubo un problema al interpretar la decisión para el siguiente paso."
            new_messages_for_state.append(AIMessage(content=error_msg_content))
            return {"messages": new_messages_for_state, "next_agent": "error_handler"}

    except Exception as e:
        print(f"Error crítico en el supervisor_node_iterative: {e}")
        import traceback
        traceback.print_exc()
        return {"messages": [AIMessage(content=f"Supervisor: Se produjo un error grave al procesar tu solicitud.")], "next_agent": "error_handler"}
