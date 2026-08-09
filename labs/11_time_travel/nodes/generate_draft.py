"""
Node: generate_draft
Nhiệm vụ: Viết bản nháp (draft) dựa trên dàn ý (outline) nhận được từ state.
Đầu vào: WriterState (chứa 'topic', 'outline')
Đầu ra: dict cập nhật trường 'draft'
"""
from ..state import WriterState
from shared.models import GroqLLMModel

def generate_draft(state: WriterState) -> dict:
    llm = GroqLLMModel()
    
    topic = state.get("topic")
    outline = state.get("outline")
    
    prompt = f"""Bạn là trợ lý viết nội dung chuyên nghiệp.
Viết bản nháp từ chủ đề và dàn ý sau.

Chủ đề: {topic}
Dàn ý: {outline}

Yêu cầu:
- Viết trực tiếp nội dung, không thêm lời dẫn hoặc giải thích.
- Văn phong rõ ràng, tự nhiên, chuyên nghiệp.
- Độ dài gọn: 3-5 đoạn ngắn.
- Không dùng tiêu đề nếu người dùng không yêu cầu."""
    response = llm.invoke(prompt)
    return {"draft": response.content}
    
if __name__ == "__main__":
    state = {
        "topic": "Thư chúc mừng bạn thân",
        "outline": "1. Lời mở đầu cảm ơn lời chúc.\n2. Chia sẻ cảm xúc vui mừng và tình trạng công việc hiện tại.\n3. Lời chúc sức khỏe và hẹn gặp lại."
    }
    data = generate_draft(state)
    print(data.get("draft"))