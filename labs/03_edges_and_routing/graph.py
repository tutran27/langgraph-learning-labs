import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, START, END
from state import RouterState
from nodes.classify import classify_node
from nodes.process_text import process_text_node
from nodes.process_number import process_number_node
from nodes.reject import reject_node
from routers import route_input

builder = StateGraph(RouterState)

builder.add_node("classify", classify_node)
builder.add_node("process_text", process_text_node)
builder.add_node("process_number", process_number_node)
builder.add_node("reject", reject_node)

builder.add_edge(START, "classify")

builder.add_conditional_edges(
    "classify",
    route_input,
    {
        "process_text": "process_text",
        "process_number": "process_number",
        "reject": "reject"
    }
)

builder.add_edge("process_text", END)
builder.add_edge("process_number", END)
builder.add_edge("reject", END)

graph = builder.compile()
