from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from state import SQLAgentState
from nodes.generate_sql import generate_sql
from nodes.execute_sql import execute_sql
from nodes.sql_corrector import sql_corrector
from nodes.schema_explorer import schema_explorer
from nodes.generate_answer import generate_answer

builder = StateGraph(SQLAgentState)

builder.add_node("generate_sql", generate_sql)
builder.add_node("execute_sql", execute_sql)
builder.add_node("sql_corrector", sql_corrector)
builder.add_node("schema_explorer", schema_explorer)
builder.add_node("generate_answer", generate_answer)

builder.add_edge(START, "generate_sql")
builder.add_edge("generate_answer", END)

graph = builder.compile(checkpointer=MemorySaver())

