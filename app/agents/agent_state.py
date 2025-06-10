from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    # next_agent: str # Para que el orquestador sepa a quién pasar el control
    # current_task_description: str
    location:str