from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .state import ApprovalState

def decide_next_step(state: ApprovalState):
    approved = state.get("approved")
    if approved in ["y", "yes", "có", "ok"]:
        return "execute_action"
    elif approved in ["n", "no", "không", "ko"]:
        return "reject_action"
    else:
        return "request_approval"