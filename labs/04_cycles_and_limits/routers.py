from typing import Literal
from langgraph.graph import END
from state import CodeWriterState

def route_evaluation(state: CodeWriterState) -> Literal["revise", "end"]:
    print(f"--- [Router] route_evaluation: attempts={state.get('attempts', 0)}/{state.get('max_attempts', 3)} ---")
    
    if state.get("is_correct", False):
        return "end"
        
    attempts = state.get("attempts", 0)
    max_attempts = state.get("max_attempts", 3)
    
    if attempts >= max_attempts:
        return "end"
        
    return "revise"
