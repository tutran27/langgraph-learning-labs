from langgraph.graph import END, START, StateGraph

from .state import ValidationState
from .nodes import check_inventory, validate_address, validate_customer

builder = StateGraph(ValidationState)

builder.add_node("check_inventory", check_inventory)
builder.add_node("validate_address", validate_address)
builder.add_node("validate_customer", validate_customer)

builder.add_edge(START, "check_inventory")
builder.add_edge("check_inventory", "validate_address")
builder.add_edge("validate_address", "validate_customer")
builder.add_edge("validate_customer", END)

validation_subgraph = builder.compile()

if __name__ == "__main__":
    import json
    state = {
        "order_id": "ORD-001",
        "customer_name": "John Doe",
        "customer_email": "john.doe@email.com",
        "customer_address": "123 Main St, TP.HCM",
        "items": [
            {"name": "Laptop Dell XPS 15", "quantity": 1},
            {"name": "Chuột Logitech MX Master", "quantity": 1},
        ],
    }

    print("=" * 60)
    print("============== STREAMING VALIDATION ==============")
    print("=" * 60)

    for s in validation_subgraph.stream(state):
        print(json.dumps(s, indent=2, ensure_ascii=False))

    print("=" * 60)
    print("============== FINAL STATE ==============")
    result = validation_subgraph.invoke(state)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 60)