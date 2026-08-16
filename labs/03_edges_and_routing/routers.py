from typing import Literal
from state import RouterState

def route_input(state: RouterState) -> Literal["process_text", "process_number", "reject"]:
    input_type = state.get("input_type")
    print(f"--- [Router] route_input: input_type={input_type} ---")
    
    if input_type == "text":
        return "process_text"
    elif input_type == "number":
        return "process_number"
    else:
        return "reject"
