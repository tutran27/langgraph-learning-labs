import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
lab_dir = os.path.dirname(current_dir)
sys.path.insert(0, lab_dir)

from langgraph.checkpoint.memory import InMemorySaver
from graph import create_graph

def test_history_traversal():
    """Kiểm tra khả năng lưu trữ và truy vấn lịch sử qua các checkpoint."""
    checkpointer = InMemorySaver()
    builder = create_graph()
    app = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "thread-history-test"}}

    # Chạy lượt 1
    res1 = app.invoke({"query": "Lượt 1", "messages": []}, config)

    # Chạy lượt 2
    res2 = app.invoke({"query": "Lượt 2", "messages": res1["messages"]}, config)

    # Lấy lịch sử checkpoint (get_state_history trả về generator ngược từ mới nhất về cũ nhất)
    history = list(app.get_state_history(config))

    # Đảm bảo lưu đúng lịch sử các lượt
    assert len(history) >= 2
    
    # Kiểm tra xem lịch sử có lưu giữ cả Lượt 1 và Lượt 2 hay không
    queries = [checkpoint.values.get("query") for checkpoint in history]
    assert "Lượt 2" in queries
    assert "Lượt 1" in queries
