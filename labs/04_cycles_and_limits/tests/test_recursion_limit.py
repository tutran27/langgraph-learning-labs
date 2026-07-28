import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from langgraph.errors import GraphRecursionError
from unittest.mock import MagicMock
from langgraph.graph import StateGraph, START, END
from state import CodeWriterState
from nodes.generate import generate_code_node
from nodes.revise import revise_code_node
from routers import route_evaluation

def test_graph_recursion_limit():
    # Tạo mock evaluate node trực tiếp bằng MagicMock để luôn báo lỗi (tạo vòng lặp vô hạn)
    mock_eval = MagicMock()
    mock_eval.return_value = {
        "is_correct": False,
        "feedback": "Forced failure for testing recursion_limit",
        "stop_reason": None
    }
    
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
        "max_attempts": 100  # Cấu hình max_attempts lớn để ưu tiên đụng giới hạn đệ quy của LangGraph trước
    }
    
    # Đặt cấu hình recursion_limit là 3
    config = {"recursion_limit": 3}
    
    with pytest.raises(GraphRecursionError):
        test_graph.invoke(initial_state, config=config)
