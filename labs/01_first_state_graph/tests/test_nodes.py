from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage
from nodes import format_conversation_node, summarize_conversation_node, qa_conversation_node

def test_format_conversation_node():
    state = {
        "messages": [
            HumanMessage(content="Hello"),
            AIMessage(content="Hi there!")
        ]
    }
    result = format_conversation_node(state)
    assert result == {"conversation_text": "Human: Hello\nAI: Hi there!\n"}

@patch("nodes.llm")
def test_summarize_conversation_node(mock_llm):
    mock_llm.invoke.return_value = MagicMock(content="Bản tóm tắt mẫu.")
    
    state = {"conversation_text": "Human: Hello\nAI: Hi there!\n"}
    result = summarize_conversation_node(state)
    assert result == {"summary": "Bản tóm tắt mẫu."}

@patch("nodes.llm")
def test_qa_conversation_node(mock_llm):
    mock_llm.invoke.return_value = MagicMock(content="Câu trả lời mẫu.")
    
    state = {"summary": "Bản tóm tắt mẫu.", "question": "Hỏi?"}
    result = qa_conversation_node(state)
    assert result == {"answer": "Câu trả lời mẫu."}
