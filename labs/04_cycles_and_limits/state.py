from typing import TypedDict, List, Dict, Any, Optional

class CodeWriterState(TypedDict):
    task_description: str
    test_cases: List[Dict[str, Any]]
    code: str
    feedback: str
    attempts: int
    max_attempts: int
    is_correct: bool
    stop_reason: Optional[str]
