import sys
import os
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# Thêm thư mục hiện tại vào PYTHONPATH để tránh lỗi import
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from graph import create_graph

DB_PATH = os.path.join(current_dir, "persistence", "state.db")

def main():
    print("--- Get Current State ---")

    if not os.path.exists(DB_PATH):
        print(f"Error: Database file not found at {DB_PATH}")
        print("Please run persistence/sqlite.py first.")
        return

    # 1. Kết nối DB và compile graph với SqliteSaver
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        checkpointer = SqliteSaver(conn)
        builder = create_graph()
        app = builder.compile(checkpointer=checkpointer)

        # 2. Truy vấn trạng thái hiện tại của thread-shared
        config = {"configurable": {"thread_id": "thread-shared"}}
        state = app.get_state(config)

        if not state.values:
            print("Thread 'thread-shared' has no state saved.")
            return

        # 3. In thông tin chi tiết của Checkpoint hiện tại
        print(f"Thread ID: {config['configurable']['thread_id']}")
        print(f"Checkpoint ID: {state.config['configurable'].get('checkpoint_id')}")
        print(f"Next Node: {state.next}")
        print(f"Metadata: {state.metadata}")
        
        print("\nState Values:")
        print(f"  Query: {state.values.get('query')}")
        print(f"  Response: {state.values.get('response').content if state.values.get('response') else None}")
        
        print("\nMessages History:")
        for msg in state.values.get("messages", []):
            print(f"  {msg.type.upper()}: {msg.content}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()