from langgraph.graph import StateGraph, START, END
from state import GraphState
from nodes import (
    format_conversation_node,
    summarize_conversation_node,
    qa_conversation_node,
)

builder = StateGraph(GraphState)

builder.add_node("format_conversation", format_conversation_node)
builder.add_node("summarize_conversation", summarize_conversation_node)
builder.add_node("qa_conversation", qa_conversation_node)

builder.add_edge(START, "format_conversation")
builder.add_edge("format_conversation", "summarize_conversation")
builder.add_edge("summarize_conversation", "qa_conversation")
builder.add_edge("qa_conversation", END)

graph = builder.compile()
