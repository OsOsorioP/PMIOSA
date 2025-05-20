from pydantic import BaseModel
from typing import List, Optional

class ChatMessageInput(BaseModel):
    role: str
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None

class ChatRequest(BaseModel):
    original_query: str
    messages_history: List[ChatMessageInput] = []
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response_messages: List[ChatMessageInput]
    final_state_messages: List[ChatMessageInput]
    session_id: Optional[str] = None