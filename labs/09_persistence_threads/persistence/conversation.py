import sys
import os
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from graph import create_graph


DB_PATH = os.path.join(current_dir, "conversation_db.db")

def main():
    print("====================================================")
    print("=== CHẠY THỬ NGHIỆM SQLITE SAVER ===")
    print("====================================================\n")

    conn=sqlite3.connect(DB_PATH,check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    builder = create_graph()
    app = builder.compile(checkpointer=checkpointer)

    config_1 = {"configurable": {"thread_id": "thread-2"}}

    while True:
        input_user = input("User: ")
        if input_user in ["q", "exit", "quit", "bye"]:
            break
        state_1 = {"query": input_user, "messages": []}
        res_1 = app.invoke(state_1, config_1)
        print("Bot:", res_1["response"].content)

    conn.close()

if __name__ == "__main__":
    main()
