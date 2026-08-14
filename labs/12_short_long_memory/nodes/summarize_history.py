from shared.models import GroqLLMModel
from langgraph.runtime import Runtime

from ..context import Context
from ..state import State


def message_to_str(messages):
    res = ""
    for message in messages:
        res += f"{message.type}: {message.content}\n"
    return res


def summarize_history(state: State, runtime: Runtime[Context]):
    messages = state["messages"]
    if len(messages) <= 1:
        return {"summary": ""}
    else:
        llm = GroqLLMModel()
        str_messages = message_to_str(messages[-8:])

        prompt = f"""
        Hãy tóm tắt các đoạn hội thoại sau đây giữ nguyên các ý chính và nội dung quan trọng dưới dạng gạch đầu dòng.
        {str_messages}
        """
        res = llm.invoke(prompt)
        return {"summary": res.content}


    
