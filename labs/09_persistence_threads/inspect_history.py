import sys
import os
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from langgraph.checkpoint.sqlite import SqliteSaver
from graph import create_graph

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persistence", "state.db")

def main():
    print("--- Get State History ---")

    if not os.path.exists(DB_PATH):
        print(f"Error: Database file not found at {DB_PATH}")
        print("Please run persistence/sqlite.py first.")
        return

    # 1. Kết nối DB và compile graph với SqliteSaver
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        memory = SqliteSaver(conn)
        builder = create_graph()
        graph = builder.compile(checkpointer=memory)

        # 2. Truy vấn lịch sử trạng thái của thread-shared
        config = {"configurable": {"thread_id": "thread-shared"}}
        history = list(graph.get_state_history(config))

        print(f"Found {len(history)} checkpoint(s) for thread '{config['configurable']['thread_id']}':\n")

        # 3. Duyệt qua từng checkpoint
        for idx, state in enumerate(history):
            print(f"Checkpoint {idx + 1}:")
            print(f"  Checkpoint ID: {state.config['configurable'].get('checkpoint_id')}")
            print(f"  Next: {state.next}")
            print(f"  Metadata: {state.metadata}")
            
            # Hiển thị các giá trị trong State
            print("  Values:")
            for k, v in state.values.items():
                if k == "messages":
                    print(f"    - messages ({len(v)}):")
                    for msg in v:
                        print(f"      {msg.type.upper()}: {msg.content}")
                else:
                    print(f"    - {k}: {v}")
            print("-" * 30)

    finally:
        conn.close()

if __name__ == "__main__":
    main()
