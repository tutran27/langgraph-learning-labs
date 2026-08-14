from typing import TypedDict

class ProgressUpdate(TypedDict):
    percentage: int
    status: str

def progress_reducer(current: ProgressUpdate | None, 
                     new: ProgressUpdate | None) -> ProgressUpdate:
    if new is None:
        return current or {"percentage": 0, 
                           "status": "Not started"}
    return new
