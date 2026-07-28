import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, START, END
from state import CodeWriterState
from nodes.generate import generate_code_node
from nodes.evaluate import evaluate_code_node
from nodes.revise import revise_code_node
from routers import route_evaluation

builder = StateGraph(CodeWriterState)

builder.add_node("generate", generate_code_node)
builder.add_node("evaluate", evaluate_code_node)
builder.add_node("revise", revise_code_node)

builder.add_edge(START, "generate")
builder.add_edge("generate", "evaluate")

builder.add_conditional_edges(
    "evaluate",
    route_evaluation,
    {
        "revise": "revise",
        "end": END
    }
)

builder.add_edge("revise", "evaluate")

graph = builder.compile()
