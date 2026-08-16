import sys
import os
# Thêm thư mục hiện tại vào path để import các file local trơn tru
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage, AIMessage
from graph import graph

if __name__ == "__main__":
    mock_messages = [
        HumanMessage(content="Chào bạn, mình muốn hỏi thông tin đặt phòng cho 2 người lớn vào ngày 5/8 tới."),
        AIMessage(content="Chào bạn! Mình có phòng Deluxe (1.500.000đ/đêm) và Standard (1.000.000đ/đêm). Bạn muốn chọn loại nào ạ?"),
        HumanMessage(content="Cho mình chọn phòng Deluxe nhé. Khách sạn có bể bơi và chỗ đỗ xe ô tô không bạn?"),
        AIMessage(content="Dạ có, khách sạn có bể bơi ngoài trời miễn phí và bãi đỗ xe ô tô rộng rãi cho khách lưu trú ạ."),
        HumanMessage(content="Ok cám ơn bạn, mình sẽ đặt Deluxe. Bạn note lại giúp mình thông tin này nhé."),
    ]
    
    test_question = "Khách chọn loại phòng gì, đi vào ngày nào, và khách sạn có bãi đỗ xe ô tô không?"

    initial_state = {
        "messages": mock_messages,
        "question": test_question,
    }

    print("=== BẮT ĐẦU CHẠY GRAPH ===")
    
    final_state = graph.invoke(initial_state)
    
    print("\n=== KẾT QUẢ CUỐI CÙNG ===")
    print("\n--- 1. Văn bản hội thoại phẳng (conversation_text) ---")
    print(final_state.get("conversation_text"))
    
    print("--- 2. Bản tóm tắt thông tin quan trọng (summary) ---")
    print(final_state.get("summary"))
    
    print("\n--- 3. Câu trả lời cho câu hỏi (answer) ---")
    print(f"Câu hỏi: {test_question}")
    print(f"Trả lời: {final_state.get('answer')}")
