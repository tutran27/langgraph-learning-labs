from state import RouterState

def classify_node(state: RouterState):
    input_data = state.get("input_data")
    print(f"--- [Node] classify_node: input_data={input_data} ---")
    
    if isinstance(input_data, str):
        return {
            "input_type": "text",
            "routing_reason": f"Input '{input_data}' is a string, routing to process_text."
        }
    elif isinstance(input_data, (int, float)) and not isinstance(input_data, bool):
        return {
            "input_type": "number",
            "routing_reason": f"Input {input_data} is a number, routing to process_number."
        }
    else:
        return {
            "input_type": "unsupported",
            "routing_reason": f"Input type {type(input_data).__name__} is not supported, routing to reject."
        }
