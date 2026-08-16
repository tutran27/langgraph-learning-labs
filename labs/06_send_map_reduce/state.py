from typing import Annotated, TypedDict, List, Dict, Any
from reducers import merge_analyses

class OverallState(TypedDict):
    document_path: str
    document: str
    chunks: List[str]
    analyses: Annotated[List[Dict[str, Any]], merge_analyses]
    final_report: str
