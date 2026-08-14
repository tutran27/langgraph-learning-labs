from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from custom_channels import ProgressUpdate, progress_reducer

class ResearchSubgraphState(TypedDict):
    topic: str
    queries: List[str]
    documents: List[str]
    progress: Annotated[ProgressUpdate, progress_reducer]

class ParentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    topic: str
    documents: List[str]
    progress: Annotated[ProgressUpdate, progress_reducer]
