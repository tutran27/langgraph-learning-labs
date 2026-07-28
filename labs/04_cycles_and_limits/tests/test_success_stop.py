import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import graph

def test_graph_success_stop():
    initial_state = {
        "task_description": "Write a Python function 'add_numbers(x, y)' that returns the sum of x and y.",
        "test_cases": [
            {"input": (2, 3), "expected": 5},
            {"input": (-1, 1), "expected": 0}
        ],
        "attempts": 0,
        "max_attempts": 3
    }
    
    result = graph.invoke(initial_state)
    
    assert result["is_correct"] is True
    assert result["stop_reason"] == "success"
    assert "add_numbers" in result["code"]
