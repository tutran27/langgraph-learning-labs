from langgraph.graph import StateGraph, START, END
from .state import PaymentState
from .nodes import calculate_node, process_payment, verify_payment

builder = StateGraph(PaymentState)

builder.add_node("calculate_total", calculate_node)
builder.add_node("process_payment", process_payment)
builder.add_node("verify_payment", verify_payment)

builder.add_edge(START, "calculate_total")
builder.add_edge("calculate_total", "process_payment")
builder.add_edge("process_payment", "verify_payment")
builder.add_edge("verify_payment", END)

payment_subgraph = builder.compile()

if __name__ == "__main__":
    import json

    state = {
        "order_id": "ORD-001",
        "customer_name": "Nguyễn Văn An",
        "customer_email": "an.nguyen@email.com",
        "items": [
            {"name": "Laptop Dell XPS 15", "quantity": 1, "unit_price": 35000000},
            {"name": "Chuột Logitech MX Master", "quantity": 2, "unit_price": 2500000},
        ],
        "card_token": "",
        "transaction_id": "",
        "gateway_response": "",
        "total_amount": 0,
        "payment_success": False,
        "logs": [],
    }

    print("=" * 60)
    print("============== STREAMING PAYMENT ==============")
    print("=" * 60)
    for s in payment_subgraph.stream(state):
        print(json.dumps(s, indent=2, ensure_ascii=False))

    print("=" * 60)
    print("============== FINAL STATE ==============")
    result = payment_subgraph.invoke(state)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 60)
