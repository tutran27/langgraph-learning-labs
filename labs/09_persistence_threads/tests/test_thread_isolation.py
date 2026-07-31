import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
lab_dir = os.path.dirname(current_dir)
sys.path.insert(0, lab_dir)

from langgraph.checkpoint.memory import InMemorySaver
from graph import create_graph

def test_thread_isolation():
    """Kiểm tra tính cô lập giữa các thread khác nhau."""
    checkpointer = InMemorySaver()
    builder = create_graph()
    app = builder.compile(checkpointer=checkpointer)

    config_1 = {"configurable": {"thread_id": "thread-1"}}
    config_2 = {"configurable": {"thread_id": "thread-2"}}

    # Chạy trên Thread 1
    app.invoke({"query": "Tôi là Alice", "messages": []}, config_1)
    
    # Chạy trên Thread 2
    app.invoke({"query": "Tôi là Bob", "messages": []}, config_2)

    # Lấy trạng thái của từng thread
    state_1 = app.get_state(config_1)
    state_2 = app.get_state(config_2)

    # Kiểm tra tính cô lập
    assert state_1.values["query"] == "Tôi là Alice"
    assert state_2.values["query"] == "Tôi là Bob"
