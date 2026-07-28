from state import RouterState

def reject_node(state: RouterState):
    input_data = state.get("input_data")
    print(f"--- [Node] reject_node ---")
    
    result = f"Rejected: Input format '{type(input_data).__name__}' is not supported."
    return {"processed_result": result}
