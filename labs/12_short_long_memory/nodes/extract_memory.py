import json
import re
from langgraph.runtime import Runtime
from shared.models import GroqLLMModel

from ..context import Context
from ..memory.namespaces import get_user_memory_namespace
from ..memory.policies import should_save_memory
from ..state import State


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


def extract_memory(state: State, runtime: Runtime[Context]):
    store = runtime.store
    user_id = runtime.context.user_id
    namespace = get_user_memory_namespace(user_id)

    llm = GroqLLMModel()
    str_messages = "\n".join([f"{m.type}: {m.content}" for m in state["messages"][-8:]])

    prompt = f"""
    Kiểm tra xem nội dung sau đây có chứa những thông tin quan trọng, xứng đáng để lưu lại để phục vụ cho việc trả lời các câu hỏi sau này hay ko.
    Nếu có thì tóm tắt lại các thông tin quan trọng đó. Nếu không có gì thì để summary là rỗng.
    {str_messages}

    Trả về đúng JSON hợp lệ
    {{ 
        "should_save": true/false,
        "summary": "<summary>"
    }}
    """
    response = llm.invoke(prompt)
    data = json_extract(response.content)
    if not data:
        return {
            "should_save": False,
            "summary": ""
        }

    should_save = data.get("should_save", False)
    summary = data.get("summary", "")

    if should_save_memory(should_save, summary):
        store.put(namespace, "fact", {"text": summary})

    return data


