from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from app.models.models import ChatMessageInput # Importa desde el mismo directorio api

def convert_to_langchain_message(msg_input: ChatMessageInput) -> BaseMessage:
    # (COPIA AQUÍ TU FUNCIÓN convert_to_langchain_message COMPLETA)
    if msg_input.role == "human":
        return HumanMessage(content=msg_input.content)
    # ... (resto de la lógica)
    return HumanMessage(content=f"({msg_input.role}): {msg_input.content}")


def convert_from_langchain_message(lc_msg: BaseMessage) -> ChatMessageInput:
    # (COPIA AQUÍ TU FUNCIÓN convert_from_langchain_message COMPLETA)
    role = "unknown"
    content = str(lc_msg.content) if hasattr(lc_msg, 'content') else ""
    # ... (resto de la lógica)
    return ChatMessageInput(role=role, content=content)