import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from state import ResearchSubgraphState, ParentState
from nodes import generate_queries_node, fetch_documents_node, synthesize_node

def create_graph():
    subgraph_builder = StateGraph(ResearchSubgraphState)
    subgraph_builder.add_node("generate_queries", generate_queries_node)
    subgraph_builder.add_node("fetch_documents", fetch_documents_node)
    subgraph_builder.add_edge(START, "generate_queries")
    subgraph_builder.add_edge("generate_queries", "fetch_documents")
    subgraph_builder.add_edge("fetch_documents", END)
    subgraph = subgraph_builder.compile()
    
    parent_builder = StateGraph(ParentState)
    parent_builder.add_node("research", subgraph)
    parent_builder.add_node("synthesize", synthesize_node)
    parent_builder.add_edge(START, "research")
    parent_builder.add_edge("research", "synthesize")
    parent_builder.add_edge("synthesize", END)
    
    checkpointer = MemorySaver()
    return parent_builder.compile(checkpointer=checkpointer)

graph = create_graph()
