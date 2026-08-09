"""
Node: refine_draft
Nhiệm vụ: Đánh bóng và hoàn thiện bản nháp (draft) nhận được từ state để tạo ra bài viết cuối cùng (final_text).
Đầu vào: WriterState (chứa 'topic', 'draft')
Đầu ra: dict cập nhật trường 'final_text'
"""
from ..state import WriterState
from shared.models import GroqLLMModel

def refine_draft(state: WriterState) -> dict:
    llm = GroqLLMModel()
    
    topic = state.get("topic")
    draft = state.get("draft")
    
    prompt = f"""Bạn là biên tập viên nội dung chuyên nghiệp.
Tinh chỉnh bản nháp sau để văn bản rõ ràng, tự nhiên và gọn hơn.

Chủ đề: {topic}
Bản nháp:
{draft}

Yêu cầu:
- Giữ nguyên ý chính và sắc thái ban đầu.
- Loại bỏ câu thừa, diễn đạt rườm rà và văn phong máy móc.
- Trả về trực tiếp văn bản hoàn chỉnh, không thêm nhận xét hoặc giải thích.
- Độ dài vừa đủ, không lan man."""
    response = llm.invoke(prompt)
    return {"final_text": response.content}

if __name__ == "__main__":
    state = {
        "topic": "Thư chúc mừng bạn thân",
        "draft": "Chào bạn, Cảm ơn bạn đã chúc mừng mình nhé. Mình rất vui. Dạo này mình cũng khỏe. Khi nào rảnh gặp nhau nha. Chúc bạn sức khỏe."
    }
    data = refine_draft(state)
    print(data.get("final_text"))
