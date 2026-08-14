import pytest
from unittest.mock import patch
from langchain_community.chat_models import FakeListChatModel

# Nhập từ thư mục cục bộ của Lab 13
from graph import create_graph

@pytest.mark.asyncio
async def test_message_streaming():
    # Tạo fake LLM trả về kết quả giả lập tương thích với stream
    fake_llm = FakeListChatModel(responses=["Báo cáo nghiên cứu mẫu về AI."])
    
    with patch("nodes.llm.groq_chat", return_value=fake_llm):
        app = create_graph()
        inputs = {"topic": "AI Testing"}
        config = {"configurable": {"thread_id": "test_msg_stream_thread"}}
        
        chunks = []
        async for msg, metadata in app.astream(inputs, config, stream_mode="messages"):
            chunks.append((msg, metadata))
            
        # Xác minh đã nhận các tin nhắn được stream
        assert len(chunks) > 0
        
        # Xác minh nguồn phát ra từ node 'synthesize'
        synthesize_events = [meta for msg, meta in chunks if meta.get("langgraph_node") == "synthesize"]
        assert len(synthesize_events) > 0
