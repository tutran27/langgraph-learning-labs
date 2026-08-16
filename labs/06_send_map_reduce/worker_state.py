from typing import TypedDict

class WorkerState(TypedDict):
    chunk_id: int
    chunk_text: str
