from shared.models import GroqLLMModel
from ..state import State
from langchain_core.messages import AIMessage, HumanMessage


def chat_node(state: State):
    llm = GroqLLMModel()
    query = state["query"]

    recent_messages = state["recent_messages"]
    retrieved_memories = state["retrieved_memories"]

    if retrieved_memories:
        prompt = f"""
        Trả lời câu hỏi sau:
        {query}
        Các thông tin quan trọng khác có thể sử dụng để trả lời nếu liên quan: {retrieved_memories}
        """
    elif recent_messages:
        prompt = f"""
        Trả lời câu hỏi sau:
        {query}
        Các tin nhắn gần đây: {recent_messages}
        """
    else:
        prompt = f"""
        Trả lời câu hỏi sau:
        {query}
        """
    answer = llm.invoke(prompt)

    return {
        "answer": answer.content,
        "messages": [
            HumanMessage(content=query),
            AIMessage(content=answer.content),
        ],
    }


if __name__ == "__main__":
    state = State(
        query="xin chào",
        answer="",
        messages=[],
        retrieved_memories="",
        summary="",
        recent_messages="",
    )
    state = chat_node(state)
    print(state)