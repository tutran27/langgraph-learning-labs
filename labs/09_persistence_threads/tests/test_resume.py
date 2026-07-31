import sys
import os
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))
lab_dir = os.path.dirname(current_dir)
sys.path.insert(0, lab_dir)

from langgraph.checkpoint.sqlite import SqliteSaver
from graph import create_graph

DB_PATH = os.path.join(current_dir, "test_persistence.db")

def test_sqlite_persistence():
    """Kiểm tra tính bền vững của SQLite Saver khi tắt tiến trình và kết nối lại."""
    # Dọn dẹp trước khi chạy
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    config = {"configurable": {"thread_id": "thread-test-resume"}}

    # Lượt 1: Giả lập chạy lần đầu và ghi dữ liệu xuống DB
    conn1 = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        checkpointer1 = SqliteSaver(conn1)
        app1 = create_graph().compile(checkpointer=checkpointer1)
        res1 = app1.invoke({"query": "Hello, I am Alice.", "messages": []}, config)
        messages_count = len(res1["messages"])
    finally:
        conn1.close()

    # Lượt 2: Kết nối lại (giả lập tiến trình mới chạy lại) và đọc dữ liệu
    conn2 = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        checkpointer2 = SqliteSaver(conn2)
        app2 = create_graph().compile(checkpointer=checkpointer2)
        state = app2.get_state(config)
        
        # Kiểm tra trạng thái đã lưu có được khôi phục thành công không
        assert state.values["query"] == "Hello, I am Alice."
        assert len(state.values["messages"]) == messages_count
    finally:
        conn2.close()

    # Dọn dẹp DB kiểm thử
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
