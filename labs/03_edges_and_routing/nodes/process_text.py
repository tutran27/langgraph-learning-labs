from state import RouterState

def process_text_node(state: RouterState):
    input_data = state.get("input_data", "")
    print(f"--- [Node] process_text_node ---")
    
    is_critical = any(word in input_data.upper() for word in ["CRITICAL", "ERROR", "FAIL", "EXCEPTION"])
    level = "HIGH" if is_critical else "NORMAL"
    
    result = f"Processed text log. Level: {level}. Original content: '{input_data}'"
    return {"processed_result": result}
