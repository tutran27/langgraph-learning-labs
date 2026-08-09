import operator

from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages, BaseMessage   
# tạo class state 
class State(TypedDict):
    """
    Trạng thái hội thoại.
    """
    query:str
    answer:str
    messages: Annotated[List[BaseMessage],add_messages]
    retrieved_memories:str
    summary:str
    
    recent_messages:str
