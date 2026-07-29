import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nodes.analyze_chunk import analyze_chunk_node

def test_worker_state_node():
    worker_input = {
        "chunk_id": 1,
        "chunk_text": "Doanh thu quý 1 đạt 100 tỷ đồng."
    }
    result = analyze_chunk_node(worker_input)
    assert "analyses" in result
    assert len(result["analyses"]) == 1
    assert result["analyses"][0]["chunk_id"] == 1
