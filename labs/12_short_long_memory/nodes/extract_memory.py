from shared.models import GroqLLMModel
from ..state import State
import re
import json 
from langgraph.runtime import Runtime

from ..context import Context

def json_extract(response: str):
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

def extract_memory(state: State, runtime:Runtime[Context]):
    store=runtime.store
    user_id=runtime.context.user_id
    namespace=("memories",user_id)

    llm=GroqLLMModel()
    answer=state["answer"]
    prompt=f"""
    Kiểm tra xem nội dung sau đây có chứa những thông tin qua trọng, xứng đáng để lưu lại để phục vụ cho việc trả lời các câu hỏi sau này hay ko.
    Nếu có thì tóm tắt lại các thông tin quan trọng đó. Nếu không có gì thì để summary là rỗng.
    {answer}

    Trả về đúng JSON hợp lệ
    {{ 
        "should_save": true/false,
        "summary": "<summary>"
    }}
    """
    response=llm.invoke(prompt)
    data=json_extract(response.content)
    if not data:
        return {
            "should_save": False,
            "summary": ""
        }
    if data.get("should_save") and data.get("summary"):
        store.put(namespace, "fact", {"text": data.get("summary")})
    return data
