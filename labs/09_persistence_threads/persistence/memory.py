import sys
import os
from langgraph.checkpoint.memory import InMemorySaver

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from graph import create_graph

def main():
    print("====================================================")
    print("=== CHẠY THỬ NGHIỆM IN-MEMORY SAVER (TRONG RAM) ===")
    print("====================================================\n")

    checkpointer = InMemorySaver()
    builder = create_graph()
    app = builder.compile(checkpointer=checkpointer)

    config_1 = {"configurable": {"thread_id": "thread-1"}}

    print("--- Lượt 1 (Thread 1): User hỏi 'Tôi là Alice' ---")
    state_1 = {"query": "Tôi là Alice", "messages": []}
    res_1 = app.invoke(state_1, config_1)
    print("Bot:", res_1["response"].content)

    print("\n--- Lượt 2 (Thread 1): User hỏi 'Tên tôi là gì?' ---")
    state_2 = {"query": "Tên tôi là gì?", "messages": res_1["messages"]}
    res_2 = app.invoke(state_2, config_1)
    print("Bot:", res_2["response"].content)

    config_2 = {"configurable": {"thread_id": "thread-2"}}
    print("\n--- Lượt 3 (Thread 2): User hỏi 'Tên tôi là gì?' ---")
    state_3 = {"query": "Tên tôi là gì?", "messages": []}
    res_3 = app.invoke(state_3, config_2)
    print("Bot:", res_3["response"].content)

    print("\n⚠️ Lưu ý: Sau khi script này chạy xong, toàn bộ dữ liệu trên RAM sẽ biến mất.")
    print("====================================================")

if __name__ == "__main__":
    main()
