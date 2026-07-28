from state import RouterState

def process_number_node(state: RouterState):
    input_data = state.get("input_data", 0)
    print(f"--- [Node] process_number_node ---")
    
    status_codes = {
        200: "OK",
        201: "Created",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
        503: "Service Unavailable"
    }
    
    desc = status_codes.get(input_data, f"Unknown status code ({input_data})")
    result = f"Processed status code {input_data}: {desc}"
    return {"processed_result": result}
