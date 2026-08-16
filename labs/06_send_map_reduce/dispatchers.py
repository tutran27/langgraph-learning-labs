from langgraph.types import Send
from state import OverallState

def dispatch_analyze_chunks(state: OverallState):
    chunks = state.get("chunks", [])
    print(f"  --> [Dispatcher] Creating {len(chunks)} Send tasks for analyze_chunk node...")
    return [
        Send("analyze_chunk", {"chunk_id": i + 1, "chunk_text": chunk})
        for i, chunk in enumerate(chunks)
    ]
