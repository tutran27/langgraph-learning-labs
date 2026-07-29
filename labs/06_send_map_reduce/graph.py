import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, START, END
from state import OverallState
from dispatchers import dispatch_analyze_chunks
from nodes.split_document import split_document_node
from nodes.analyze_chunk import analyze_chunk_node
from nodes.aggregate import aggregate_node

builder = StateGraph(OverallState)

builder.add_node("split_document", split_document_node)
builder.add_node("analyze_chunk", analyze_chunk_node)
builder.add_node("aggregate", aggregate_node)

builder.add_edge(START, "split_document")

builder.add_conditional_edges(
    "split_document",
    dispatch_analyze_chunks,
    ["analyze_chunk"]
)

builder.add_edge("analyze_chunk", "aggregate")
builder.add_edge("aggregate", END)

graph = builder.compile()
