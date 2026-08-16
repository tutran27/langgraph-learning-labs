import pytest
from unittest.mock import patch
from langchain_community.chat_models import FakeListChatModel
from graph import create_graph
from event_consumer import consume_events

@pytest.mark.asyncio
async def test_custom_progress_and_events():
    fake_llm = FakeListChatModel(responses=["Báo cáo nghiên cứu mẫu về AI."])
    
    with patch("nodes.llm.groq_chat", return_value=fake_llm):
        app = create_graph()
        inputs = {"topic": "AI Progress Testing"}
        config = {"configurable": {"thread_id": "test_progress_thread"}}
        
        events = []
        async for event in consume_events(app, inputs, config):
            events.append(event)
            
        # 1. Kiểm tra sự tồn tại của custom progress events
        progress_events = [e for e in events if e["type"] == "progress"]
        assert len(progress_events) > 0
        # Tiến trình phải đạt 100% ở cuối
        assert progress_events[-1]["data"]["percentage"] == 100
        
        # 2. Kiểm tra xem các sự kiện node start/end có hoạt động không
        node_events = [e for e in events if e["type"] in ("node_start", "node_end")]
        assert len(node_events) > 0
        
        # 3. Kiểm tra xem tool lifecycle (web_search) có chạy không
        tool_starts = [e for e in events if e["type"] == "tool_start" and e["tool"] == "web_search"]
        tool_ends = [e for e in events if e["type"] == "tool_end" and e["tool"] == "web_search"]
        assert len(tool_starts) > 0
        assert len(tool_ends) > 0
        
        # 4. Kiểm tra stream tokens từ LLM
        tokens = [e for e in events if e["type"] == "token"]
        assert len(tokens) > 0
        joined_tokens = "".join([t["content"] for t in tokens])
        assert joined_tokens == "Báo cáo nghiên cứu mẫu về AI."
