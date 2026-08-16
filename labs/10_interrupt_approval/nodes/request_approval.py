from shared.models import GroqLLMModel
from ..state import ApprovalState
from langgraph.types import interrupt

def request_approval(state: ApprovalState) -> ApprovalState:
    action = state.get("action")
    query = state.get("query")

    if not action:
        return {
            "approved": "yes",
            "feedback": "Tự động duyệt cho chat thông thường"
        }

    decision=interrupt({
        "action": action,
        "message": "Hành động này cần bạn duyệt. Vui lòng phản hồi"
    })

    return {
        "approved": decision['confirmed'],
        "feedback": decision['feedback'] or None
    }
    