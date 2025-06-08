from typing import Optional
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage, SystemMessage
from app.models.models import ChatMessageInput

def convert_to_langchain_message(msg_input: ChatMessageInput) -> BaseMessage:
    if msg_input.role == "human":
        return HumanMessage(content=msg_input.content)
    elif msg_input.role == "ai":
        # Si el frontend envía un AIMessage (ej. de un turno anterior), lo convertimos.
        # No esperamos que el frontend envíe tool_calls para un AIMessage.
        return AIMessage(content=msg_input.content)
    elif msg_input.role == "system": # Si alguna vez necesitas mensajes de sistema desde el cliente
        return SystemMessage(content=msg_input.content)
    elif msg_input.role == "tool" and msg_input.name and msg_input.tool_call_id:
        return ToolMessage(content=msg_input.content, name=msg_input.name, tool_call_id=msg_input.tool_call_id)
    else:
        print(f"Advertencia: Mensaje de rol desconocido o incompleto en convert_to_langchain_message: {msg_input.role}")
        # Considera qué hacer aquí. Devolver un HumanMessage es un fallback.
        return HumanMessage(content=f"({msg_input.role} - malformado): {msg_input.content}")

def convert_from_langchain_message(lc_msg: BaseMessage) -> ChatMessageInput:
    role: str = "unknown"
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    content: str = ""

    if hasattr(lc_msg, 'content'):
        content = str(lc_msg.content)

    if isinstance(lc_msg, HumanMessage):
        role = "human"
    elif isinstance(lc_msg, AIMessage):
        role = "ai"
        # Si el AIMessage tiene tool_calls, podrías querer representarlos.
        # Por ahora, si hay tool_calls y no hay contenido, creamos una representación.
        if not content and hasattr(lc_msg, 'tool_calls') and lc_msg.tool_calls:
            tool_calls_str = ", ".join([f"{tc['name']}({tc['args']})" for tc in lc_msg.tool_calls])
            content = f"[Llamando herramientas: {tool_calls_str}]"
    elif isinstance(lc_msg, SystemMessage): # Manejar SystemMessage si se usa
        role = "system"
    elif isinstance(lc_msg, ToolMessage):
        role = "tool"
        name = lc_msg.name
        tool_call_id = lc_msg.tool_call_id
        # El contenido ya está en lc_msg.content
    
    return ChatMessageInput(role=role, content=content, name=name, tool_call_id=tool_call_id)