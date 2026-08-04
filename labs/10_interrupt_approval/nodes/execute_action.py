from shared.models import GroqLLMModel

from ..state import ApprovalState


def execute_action(state: ApprovalState) -> ApprovalState:
    action = state.get("action")
    query = state.get("query")

    if not action:
        # Nếu là chat thông thường, vẫn dùng LLM phản hồi tự nhiên
        from shared.models import GroqLLMModel
        model = GroqLLMModel()
        prompt = f"Bạn là trợ lý AI. Hãy trả lời câu hỏi/tin nhắn hội thoại này của người dùng một cách ngắn gọn, tự nhiên và thân thiện: '{query}'"
        return {
            "response": model.invoke(prompt).content
        }

    # Chỉ giả lập thực thi thành công hành động nhạy cảm, không viết code
    return {
        "response": f"✅ [Hệ thống] Thực thi thành công hành động: '{action}'."
    }
    