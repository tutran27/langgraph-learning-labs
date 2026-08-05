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
    
    prompt = f"""Bạn là một nhà biên tập văn bản có gu nghệ thuật và ngôn từ sắc sảo. Hãy tinh chỉnh và viết lại bản thảo dưới đây sao cho:
    - Ngôn từ mượt mà, tự nhiên và gần gũi như do chính con người tự viết.
    - Tuyệt đối tránh xa văn phong máy móc, rập khuôn hay các từ ngữ dịch thuật khiên cưỡng ("giả trân").
    - Giữ nguyên ý chính và cảm xúc nguyên bản nhưng hành văn tự nhiên, trôi chảy, có điểm nhấn và chiều sâu hơn.
    
    Chủ đề: {topic}
    Bản thảo nháp:
    {draft}
    
    Hãy trả về trực tiếp văn bản sau khi đã tinh chỉnh xong, không chèn thêm bất kỳ câu dẫn dắt hay lời giải thích nào khác."""
    
    response = llm.invoke(prompt)
    return {"final_text": response.content}

if __name__ == "__main__":
    state = {
        "topic": "Thư chúc mừng bạn thân",
        "draft": "Chào bạn, Cảm ơn bạn đã chúc mừng mình nhé. Mình rất vui. Dạo này mình cũng khỏe. Khi nào rảnh gặp nhau nha. Chúc bạn sức khỏe."
    }
    data = refine_draft(state)
    print(data.get("final_text"))
