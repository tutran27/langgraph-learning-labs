import json
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .state import WriterState
from .nodes.generate_outline import generate_outline
from .nodes.generate_draft import generate_draft
from .nodes.refine_draft import refine_draft

def create_graph():
    builder = StateGraph(WriterState)
    
    # Đăng ký các node
    builder.add_node("generate_outline", generate_outline)
    builder.add_node("generate_draft", generate_draft)
    builder.add_node("refine_draft", refine_draft)
    
    # Thiết lập luồng chạy tuần tự
    builder.add_edge(START, "generate_outline")
    builder.add_edge("generate_outline", "generate_draft")
    builder.add_edge("generate_draft", "refine_draft")
    builder.add_edge("refine_draft", END)
    
    # Khởi tạo Checkpointer phục vụ lưu trữ trạng thái (Time Travel)
    checkpointer = MemorySaver()
    
    # Compile đồ thị
    return builder.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    app = create_graph()
    print("Graph compiled successfully!")
    state = {"query": "Hôm qua tôi nhận được mail chúc mừng từ bạn thân. Viết mail phản hồi"}
    config = {"configurable": {"thread_id": "test_writer_session"}}
    
    result = app.invoke(state, config)
    for k, v in result.items():
        print(f"=== {k.upper()} ===")
        print(v)
        print() 