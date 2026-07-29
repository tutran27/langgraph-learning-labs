import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nodes.aggregate import aggregate_node

def test_aggregate_node():
    state = {
        "analyses": [
            {"chunk_id": 2, "summary": "Tóm tắt phần 2"},
            {"chunk_id": 1, "summary": "Tóm tắt phần 1"}
        ]
    }
    result = aggregate_node(state)
    assert "final_report" in result
    assert "📌 [Đoạn #1]: Tóm tắt phần 1" in result["final_report"]
    assert "📌 [Đoạn #2]: Tóm tắt phần 2" in result["final_report"]
