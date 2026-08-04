from shared.models import GroqLLMModel

from ..state import ApprovalState


def reject_action(state: ApprovalState) -> ApprovalState:
    action = state.get("action")
    feedback = state.get("feedback") or "Không có lý do chi tiết."

    # Chỉ giả lập từ chối hành động nhạy cảm, không viết code
    return {
        "response": f"❌ [Hệ thống] Hành động '{action}' đã bị từ chối phê duyệt. Lý do: {feedback}"
    }
    
    