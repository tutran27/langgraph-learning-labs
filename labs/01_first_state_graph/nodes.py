from langchain_core.messages import BaseMessage
from shared.models import GroqLLMModel
from state import GraphState

llm = GroqLLMModel()

def format_conversation_node(state: GraphState):
    messages = state.get("messages", [])
    formatted_text = ""
    for msg in messages:
        role = "Human" if msg.type == "human" else "AI"
        formatted_text += f"{role}: {msg.content}\n"
    print("--- [Node 1] format_conversation_node ---")
    return {"conversation_text": formatted_text}

def summarize_conversation_node(state: GraphState):
    conversation_text = state.get("conversation_text", "")
    prompt = (
        "Hãy tóm tắt ngắn gọn các thông tin quan trọng nhất "
        "từ đoạn hội thoại sau dưới dạng gạch đầu dòng:\n\n"
        f"{conversation_text}"
    )
    response = llm.invoke(prompt)
    print("--- [Node 2] summarize_conversation_node ---")
    return {"summary": response.content}

def qa_conversation_node(state: GraphState):
    summary = state.get("summary", "")
    question = state.get("question", "")
    prompt = (
        f"Dựa trên bản tóm tắt hội thoại sau đây:\n{summary}\n\n"
        f"Hãy trả lời câu hỏi sau một cách chi tiết: {question}"
    )
    response = llm.invoke(prompt)
    print("--- [Node 3] qa_conversation_node ---")
    return {"answer": response.content}
