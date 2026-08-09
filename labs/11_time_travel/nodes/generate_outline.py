"""
Node: generate_outline
Nhiệm vụ: Tạo dàn ý (outline) dựa trên chủ đề (topic) nhận được từ state.
Đầu vào: WriterState (chứa 'topic')
Đầu ra: dict cập nhật trường 'outline'
"""
import json
import re
from ..state import WriterState
from shared.models import GroqLLMModel

def extract_json(response: str):
    if not response or not isinstance(response, str):
        return None
    response = response.strip()
    try:
        return json.loads(response, strict=False)
    except Exception:
        try:
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                return json.loads(match.group(0), strict=False)
        except Exception:
            return None
    return None

def generate_outline(state: WriterState) -> dict:
    llm=GroqLLMModel()
    
    query=state.get("query")
    prompt=f"""Bạn là trợ lý viết nội dung chuyên nghiệp.
Xác định chủ đề và lập dàn ý ngắn gọn từ yêu cầu sau:
{query}

Yêu cầu:
- Trả về đúng JSON hợp lệ, không thêm giải thích.
- topic: một cụm ngắn.
- outline: 3-5 ý chính, súc tích, dễ triển khai.

Định dạng:
{{
  "topic": "<topic>",
  "outline": "<outline>"
}}"""
    response=llm.invoke(prompt)
    data=extract_json(response.content)
    if not data:
        return {
            "topic":"Không thể xác định topic",
            "outline":"Không thể xác định outline"
        }
    return data

if __name__ == "__main__":
    data=generate_outline({"query":"Hôm qua tôi nhận được mail chúc mừng từ bạn thân. Viết mail phản hồi"})
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    
