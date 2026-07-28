from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage
from graph import graph

@patch("nodes.llm")
def test_graph_execution(mock_llm):
    mock_llm.invoke.side_effect = [
        MagicMock(content="Bản tóm tắt mẫu từ đồ thị."),
        MagicMock(content="Câu trả lời mẫu từ đồ thị.")
    ]

    initial_state = {
        "messages": [
            HumanMessage(content="Hello"),
            AIMessage(content="Hi there!")
        ],
        "question": "Câu hỏi kiểm thử?"
    }

    final_state = graph.invoke(initial_state)

    assert final_state["conversation_text"] == "Human: Hello\nAI: Hi there!\n"
    assert final_state["summary"] == "Bản tóm tắt mẫu từ đồ thị."
    assert final_state["answer"] == "Câu trả lời mẫu từ đồ thị."
