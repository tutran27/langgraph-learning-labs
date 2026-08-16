import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, START, END
from state import AnalysisState
from nodes.financial_analysis import financial_analysis_node
from nodes.risk_analysis import risk_analysis_node
from nodes.technical_analysis import technical_analysis_node
from nodes.synthesize import synthesize_node

builder = StateGraph(AnalysisState)

builder.add_node("financial_analysis", financial_analysis_node)
builder.add_node("risk_analysis", risk_analysis_node)
builder.add_node("technical_analysis", technical_analysis_node)
builder.add_node("synthesize", synthesize_node)

builder.add_edge(START, "financial_analysis")
builder.add_edge(START, "risk_analysis")
builder.add_edge(START, "technical_analysis")

builder.add_edge("financial_analysis", "synthesize")
builder.add_edge("risk_analysis", "synthesize")
builder.add_edge("technical_analysis", "synthesize")

builder.add_edge("synthesize", END)

graph = builder.compile()
