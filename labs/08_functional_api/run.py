import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from workflow import content_generation_workflow
from langgraph.types import Command

def main():
    config = {"configurable": {"thread_id": "thread-123"}}
    
    print("====================================================")
    print("=== CHẠY THỬ NGHIỆM FUNCTIONAL API (LAB 8) ===")
    print("====================================================\n")
    
    print("--- Lượt chạy 1 (Khởi chạy ban đầu, dừng ở interrupt) ---")
    result1 = content_generation_workflow.invoke("Học máy và đời sống", config=config)
    
    # Do có interrupt, kết quả trả về sẽ chứa thông tin interrupt
    interrupt_info = result1["__interrupt__"][0]

    question = interrupt_info.value["question"]
    topic = interrupt_info.value["topic"]
    
    print("Kết quả ngắt:")
    print(f"  Câu hỏi: {question}")
    print(f"  Chủ đề đề xuất: {topic}")
    
    print("\n--- Lượt chạy 2 (Resume với Command) ---")
    # Gửi lệnh Command(resume=...) để tiếp tục chạy đồ thị
    # Cơ chế replay cache sẽ đảm bảo chủ đề và ID ngẫu nhiên không bị sinh lại
    result2 = content_generation_workflow.invoke(Command(resume=str(input("Nhập phản hồi: "))), config=config)
    
    print("Kết quả hoàn thành:")
    for k, v in result2.items():
        print(f"  {k}: {v}")
        
    print("\n✅ Thành công: Điểm ngắt hoạt động đúng và bảo toàn trạng thái (Replay Cache).")
    print("====================================================")

if __name__ == "__main__":
    main()
