import sys
import os
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# Thêm thư mục cha vào PYTHONPATH để import graph, state, nodes
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from graph import create_graph

DB_PATH = os.path.join(current_dir, "state.db")

def main():
    print("--- Run SQLite Saver Demo ---")

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        checkpointer = SqliteSaver(conn)
        builder = create_graph()
        app = builder.compile(checkpointer=checkpointer)

        config = {"configurable": {"thread_id": "thread-shared"}}

        current_state = app.get_state(config)

        if not current_state.values:
            print("No existing state found for thread-shared.")
            print("Turn 1:")
            state = {"query": "Tôi tên là Alice và tôi thích ăn kem.", "messages": []}
            res = app.invoke(state, config)
            print("Bot:", res["response"].content)
            print(f"\nState saved to database: {DB_PATH}")
            print("Run this script again to test persistence.")
        else:
            print("Restored state from database:")
            for msg in current_state.values["messages"]:
                print(f"  {msg.type.upper()}: {msg.content}")

            print("\nTurn 2 (Follow up):")
            state = {
                "query": "Tên tôi là gì và tôi thích ăn món gì?", 
                "messages": current_state.values["messages"]
            }
            res = app.invoke(state, config)
            print("Bot:", res["response"].content)
            print("\nSuccess: Recalled context from previous execution.")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
