from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    # Podríamos añadir más campos aquí a medida que el sistema crezca.
    # Por ejemplo:
    # next_agent: str # Para que el orquestador sepa a quién pasar el control
    # current_task_description: str