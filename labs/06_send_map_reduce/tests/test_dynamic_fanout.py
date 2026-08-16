import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dispatchers import dispatch_analyze_chunks

def test_dynamic_fanout():
    state = {
        "chunks": ["Chunk A content", "Chunk B content", "Chunk C content"]
    }
    sends = dispatch_analyze_chunks(state)
    assert len(sends) == 3
    assert sends[0].node == "analyze_chunk"
    assert sends[0].arg == {"chunk_id": 1, "chunk_text": "Chunk A content"}
    assert sends[2].arg == {"chunk_id": 3, "chunk_text": "Chunk C content"}
