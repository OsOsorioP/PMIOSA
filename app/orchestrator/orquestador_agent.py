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
     "\n\n**Proceso de Decisión ESTRICTO (sigue este orden):**\n"
     "0. **OPCIONAL** - Si la consulta del usuario es muy general sobre agricultura y no especifica una tarea clara, primero intenta responder con información general o pregunta al usuario qué aspecto específico de la agricultura le interesa antes de delegar a un agente especializado."
     "1. **PRIORIDAD MÁXIMA - Solicitar Clarificación al Usuario:** Si el ÚLTIMO mensaje en el 'Historial de la conversación actual' es un mensaje de un AGENTE (rol 'ai') Y este mensaje CONTIENE UNA PREGUNTA O SOLICITA INFORMACIÓN explícitamente para poder continuar con la 'Consulta original del usuario': Tu acción DEBE SER 'ask_user_for_clarification'. El campo 'question_for_user' DEBE contener la pregunta del agente o una reformulación clara de la misma.\n" # Modificado para ser más específico
     "2. **Responder al Usuario (Tarea Completada):** Si la 'Consulta original del usuario' ha sido COMPLETAMENTE RESPONDIDA ... (sin cambios) ...\n"
     "3. **Enrutar a Agente (Tarea Incompleta, Sin Preguntas Pendientes del Agente):** Si la 'Consulta original del usuario' NO está completamente resuelta, Y el último mensaje del agente NO es una pregunta directa para el usuario ... (sin cambios) ...\n"
     "4. **Manejo de Saludos/Consultas Genéricas:** Si la 'Consulta original del usuario' es un simple saludo ... (sin cambios) ...\n"
     "5. **Manejo de Información No Disponible:** Si el ÚLTIMO mensaje en el 'Historial de la conversación actual' es una respuesta del usuario a una pregunta de un agente, Y el usuario indica que NO PUEDE proporcionar la información solicitada (ej. 'No tengo', 'No sé'): Tu acción DEBE SER 'respond_to_user'. En 'final_answer', informa al usuario de manera concisa que sin esa información, la tarea original podría no poder completarse o se completará con limitaciones, y pregunta si desea proceder de otra manera o finalizar."
     "Asegúrate de que tu respuesta sea solo la estructura JSON de la decisión."
     "Sé conciso y directo en tu decisión. No añadas explicaciones extra a menos que sea la respuesta final al usuario."
     ),
    ("human", "Consulta original del usuario: {original_query}\n\nHistorial de la conversación actual:\n{messages}\n\nBasado en el proceso de decisión estricto, ¿cuál es tu decisión estructurada?")
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
        print(f"\nDEBUG: decision.action = '{decision.action}'")
        if decision.action == "ask_user_for_clarification":
            print(f"DEBUG: decision.question_for_user = '{decision.question_for_user}'")
        elif decision.action == "respond_to_user":
            print(f"DEBUG: decision.final_answer = '{decision.final_answer}'")
        elif decision.action == "route_to_agent":
            print(f"DEBUG: decision.next_agent_name = '{decision.next_agent_name}'")
        # --- Fin de prints de depuración ---
        print("--*****************************************************--\n")
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
