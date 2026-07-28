from typing import List
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    messages: List[BaseMessage]
    question: str
    conversation_text: str
    summary: str
    answer: str