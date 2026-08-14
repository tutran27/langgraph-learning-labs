import pytest
from unittest.mock import patch
from langchain_community.chat_models import FakeListChatModel
from graph import create_graph

@pytest.mark.asyncio
async def test_updates_and_values_streaming():
    fake_llm = FakeListChatModel(responses=["Báo cáo nghiên cứu mẫu về AI."])
    
    with patch("nodes.llm.groq_chat", return_value=fake_llm):
        app = create_graph()
        inputs = {"topic": "AI Testing"}
        config = {"configurable": {"thread_id": "test_updates_values_thread"}}
        
        # 1. Kiểm tra stream_mode="updates"
        updates = []
        async for update in app.astream(inputs, config, stream_mode="updates"):
            updates.append(update)
            
        assert len(updates) > 0
        # Cập nhật phải chứa dữ liệu của các node đã hoàn thành
        # research (subgraph) và synthesize
        has_research = any("research" in update for update in updates)
        has_synthesize = any("synthesize" in update for update in updates)
        assert has_research or has_synthesize
        
        # 2. Kiểm tra stream_mode="values"
        values = []
        async for value in app.astream(inputs, config, stream_mode="values"):
            values.append(value)
            
        assert len(values) > 0
        # Giá trị cuối cùng phải chứa câu trả lời
        final_state = values[-1]
        assert "messages" in final_state
        assert len(final_state["messages"]) > 0
        assert final_state["messages"][-1].content == "Báo cáo nghiên cứu mẫu về AI."
