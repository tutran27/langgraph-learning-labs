from typing import TypedDict
from typing_extensions import TypedDict

class WriterState(TypedDict):
    """Trạng thái của Writer Graph"""
    query: str
    topic: str
    outline: str
    draft: str
    final_text: str