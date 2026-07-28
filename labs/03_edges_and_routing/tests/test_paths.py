import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import graph

def test_text_path():
    state = {"input_data": "CRITICAL: Database offline"}
    result = graph.invoke(state)
    assert result["input_type"] == "text"
    assert "Level: HIGH" in result["processed_result"]

def test_number_path():
    state = {"input_data": 404}
    result = graph.invoke(state)
    assert result["input_type"] == "number"
    assert "Not Found" in result["processed_result"]

def test_unsupported_path():
    state = {"input_data": [1, 2, 3]}
    result = graph.invoke(state)
    assert result["input_type"] == "unsupported"
    assert "Rejected" in result["processed_result"]
