from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class ConversationState(TypedDict):
    """Trạng thái hội thoại."""
    query: str
    response: str
    messages: Annotated[list, add_messages]