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
    
    prompt = f"""Bạn là một nhà văn chuyên nghiệp. Dựa vào chủ đề (topic) và dàn ý (outline) đã có, hãy viết bản thảo nháp chi tiết bằng tiếng Việt.
    
    Chủ đề: {topic}
    Dàn ý: {outline}
    
    Hãy viết trực tiếp bài viết nháp một cách chi tiết, mạch lạc, không chèn thêm các lời bình luận ngoài lề hay tiêu đề thừa khác."""
    
    response = llm.invoke(prompt)
    return {"draft": response.content}
    
if __name__ == "__main__":
    state = {
        "topic": "Thư chúc mừng bạn thân",
        "outline": "1. Lời mở đầu cảm ơn lời chúc.\n2. Chia sẻ cảm xúc vui mừng và tình trạng công việc hiện tại.\n3. Lời chúc sức khỏe và hẹn gặp lại."
    }
    data = generate_draft(state)
    print(data.get("draft"))