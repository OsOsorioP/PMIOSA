from fastapi import APIRouter, HTTPException
from typing import List

from app.agents.graph import app_orchestrator_iterative 
from langchain_core.messages import BaseMessage 

from app.models.models import ChatRequest, ChatResponse, ChatMessageInput 
from app.utils import convert_from_langchain_message

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # (COPIA AQUÍ TU LÓGICA COMPLETA DEL ENDPOINT /chat,
    #  asegurándote de que usa app_orchestrator_iterative)
    print(f"\nRecibida solicitud de chat para query: '{request.original_query}'")
    langchain_messages: List[BaseMessage] = []
    # ... (resto de tu lógica de endpoint)
    try:
        final_orchestrator_state = app_orchestrator_iterative.invoke(
            {"messages": langchain_messages, "original_query": request.original_query}
        )
        # ... (procesamiento de la respuesta)
        api_response_messages = [convert_from_langchain_message(m) for m in final_orchestrator_state.get("messages", [])]
        
        # Determinar los mensajes de respuesta específicos de este turno
        system_reply_messages = []
        if api_response_messages:
            last_msg = api_response_messages[-1]
            # Si el último mensaje es una pregunta del supervisor o una respuesta final
            if last_msg.role == "ai":
                 system_reply_messages.append(last_msg)
            # Si no, podría ser que el flujo terminó de forma inesperada o el último mensaje es del usuario
            # (lo cual no debería pasar si el flujo termina con una respuesta de IA o pregunta)
            else:
                 system_reply_messages.append(ChatMessageInput(role="ai", content="[Procesamiento completado. Revise el historial.]"))


        return ChatResponse(
            response_messages=system_reply_messages,
            final_state_messages=api_response_messages,
            session_id=request.session_id
        )
    except Exception as e:
        # ... (manejo de excepciones)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/")
async def root_endpoint():
    return {"message": "API de Agricultura Multiagente"}