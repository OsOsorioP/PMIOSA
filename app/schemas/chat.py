from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChatInput(BaseModel):
    message: str
    conversation_id: Optional[str] = None # Para mantener el estado entre llamadas

class ChatOutputChunk(BaseModel):
    """Esquema para un trozo de la respuesta en streaming (SSE)."""
    type: str # ej: "agent_message", "tool_call", "final_answer", "error"
    data: Dict[str, Any] | str # Contenido del chunk
    conversation_id: Optional[str] = None # Devuelve el ID para la siguiente llamada