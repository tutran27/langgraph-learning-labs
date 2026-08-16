from typing import Any, Literal
from typing_extensions import TypedDict

class RouterState(TypedDict):
    input_data: Any
    input_type: Literal["text", "number", "unsupported"]
    processed_result: str
    routing_reason: str
