from langgraph.graph import StateGraph, START, END
from .state import FulfillmentState
from .nodes import assign_warehouse, create_shipment, send_notification

builder = StateGraph(FulfillmentState)

builder.add_node("assign_warehouse", assign_warehouse)
builder.add_node("create_shipment", create_shipment)
builder.add_node("send_notification", send_notification)

builder.add_edge(START, "assign_warehouse")
builder.add_edge("assign_warehouse", "create_shipment")
builder.add_edge("create_shipment", "send_notification")
builder.add_edge("send_notification", END)

fulfillment_subgraph = builder.compile()

if __name__ == "__main__":
    import json

    state = {
        "order_id": "ORD-001",
        "customer_name": "Nguyễn Văn An",
        "customer_email": "an.nguyen@email.com",
        "customer_address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
        "items": [
            {"name": "Laptop Dell XPS 15", "quantity": 1, "unit_price": 35000000},
            {"name": "Chuột Logitech MX Master", "quantity": 2, "unit_price": 2500000},
        ],
        "warehouse_id": [],
        "carriers": [],
        "estimated_delivery": "",
        "notification_sent": False,
        "tracking_id": "",
        "logs": [],
    }

    print("=" * 60)
    print("============== STREAMING FULFILLMENT ==============")
    print("=" * 60)
    for s in fulfillment_subgraph.stream(state):
        print(json.dumps(s, indent=2, ensure_ascii=False))

    print("=" * 60)
    print("============== FINAL STATE ==============")
    result = fulfillment_subgraph.invoke(state)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 60)
