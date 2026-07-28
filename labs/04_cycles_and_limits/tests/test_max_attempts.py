import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock
from langgraph.graph import StateGraph, START, END
from state import CodeWriterState
from nodes.generate import generate_code_node
from nodes.revise import revise_code_node
from routers import route_evaluation

def test_graph_max_attempts():
    # Tạo mock evaluate node trực tiếp bằng MagicMock
    mock_eval = MagicMock()
    
    def side_effect(state):
        attempts = state.get("attempts", 0)
        max_attempts = state.get("max_attempts", 2)
        stop_reason = "max_attempts_reached" if attempts >= max_attempts else None
        return {
            "is_correct": False,
            "feedback": "Forced failure for testing max_attempts",
            "stop_reason": stop_reason
        }
    mock_eval.side_effect = side_effect
    
    # Tự dựng đồ thị độc lập trong test case để tránh lỗi cache module của Python
    builder = StateGraph(CodeWriterState)
    builder.add_node("generate", generate_code_node)
    builder.add_node("evaluate", mock_eval)
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
    
    test_graph = builder.compile()
    
    initial_state = {
        "task_description": "Write a function.",
        "test_cases": [],
        "attempts": 0,
        "max_attempts": 2
    }
    
    result = test_graph.invoke(initial_state)
    
    assert result["is_correct"] is False
    assert result["attempts"] == 2
    assert result["stop_reason"] == "max_attempts_reached"
    assert mock_eval.call_count == 3
