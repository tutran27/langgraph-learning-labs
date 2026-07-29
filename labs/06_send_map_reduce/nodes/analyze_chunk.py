import json
import re

from worker_state import WorkerState
from shared.models import GroqLLMModel

def extract_json(response_text: str) -> dict:
    text = response_text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text).strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
    return {"summary": text}

def analyze_chunk_node(state: WorkerState):
    chunk_id = state.get("chunk_id", 0)
    chunk_text = state.get("chunk_text", "")
    print(f"  --> [Analyze Chunk Worker #{chunk_id}] Analyzing ({len(chunk_text)} chars)...")
    
    try:
        model = GroqLLMModel()
        prompt = f"""Bạn là một chuyên gia phân tích tài chính cao cấp.
Nhiệm vụ của bạn là đọc đoạn văn bản dưới đây và tóm tắt các ý chính/chỉ số tài chính quan trọng bằng TIẾNG VIỆT.

ĐOẠN VĂN BẢN:
{chunk_text}

QUY TẮC BẮT BUỘC:
1. Chỉ trả về ĐÚNG 1 chuỗi JSON hợp lệ.
2. KHÔNG thêm bất kỳ lời chào, giải thích, hay ký tự markdown ```json ở đầu hoặc cuối.
3. Nội dung tóm tắt phải viết bằng TIẾNG VIỆT.

ĐỊNH DẠNG JSON YÊU CẦU:
{{
    "summary": "Tóm tắt ngắn gọn thông tin tài chính nổi bật trong đoạn văn này bằng tiếng Việt."
}}
"""
        response = model.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        data = extract_json(content)
    except Exception as e:
        print(f"      [Warning] Fallback cho đoạn #{chunk_id}: {e}")
        data = {"summary": f"Tóm tắt đoạn #{chunk_id}: {chunk_text[:150]}..."}
        
    data["chunk_id"] = chunk_id
    return {"analyses": [data]}

if __name__ == "__main__":
    sample_worker_state = {
        "chunk_id": 1,
        "chunk_text": "Doanh thu năm 2023 đạt 500 tỷ VNĐ, tăng trưởng 20% so với năm 2022. Lợi nhuận trước thuế đạt 80 tỷ VNĐ."
    }
    result = analyze_chunk_node(sample_worker_state)
    print("============== Kết quả Node Analyze Chunk ==============")
    print(json.dumps(result, ensure_ascii=False, indent=2))