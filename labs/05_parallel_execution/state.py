from typing import Annotated, TypedDict, List, Dict, Any
import operator

class AnalysisState(TypedDict):
    company: str
    reports: Annotated[List[Dict[str, Any]], operator.add]
    final_summary: str
