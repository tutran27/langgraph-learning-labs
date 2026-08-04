from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

from .state import ApprovalState
from .routers import decide_next_step
from .nodes.prepare_action import prepare_action
from .nodes.request_approval import request_approval
from .nodes.execute_action import execute_action
from .nodes.reject_action import reject_action

def create_graph():
    builder=StateGraph(ApprovalState)

    builder.add_node("prepare_action", prepare_action)
    builder.add_node("request_approval", request_approval)
    builder.add_node("execute_action", execute_action)
    builder.add_node("reject_action", reject_action)

    builder.add_edge(START, "prepare_action")
    builder.add_edge("prepare_action", "request_approval")
    builder.add_conditional_edges(
        "request_approval",
        decide_next_step,
        ["execute_action", "reject_action", "request_approval"]
    )
    builder.add_edge("reject_action", END)
    builder.add_edge("execute_action", END)

    checkpointer=MemorySaver()
    graph=builder.compile(checkpointer=checkpointer)
    return graph