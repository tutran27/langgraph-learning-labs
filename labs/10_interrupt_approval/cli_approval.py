from .graph import create_graph
from langgraph.types import Command

def main():
    app = create_graph()
    config = {"configurable": {"thread_id": "chat_session_1"}}
    
    print("=== CHATBOT TƯƠNG TÁC TỰ ĐỘNG PHÊ DUYỆT (LLM) ===")
    print("- Gõ 'exit' để thoát.")
    print("- Hãy thử nhập câu hỏi thông thường (ví dụ: 'hello', 'thời tiết hôm nay')")
    print("- Hoặc yêu cầu hành động (ví dụ: 'hãy gửi email chúc mừng sinh nhật cho sếp')\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "q":
            break
        
        events = list(app.stream({"query": user_input}, config))

        state_snapshot = app.get_state(config)

        if state_snapshot.next:
            interrupts=state_snapshot.tasks[0].interrupts
            if interrupts:
                interrupt_val = interrupts[0].value
                print(f"\n⚠️  [HỆ THỐNG YÊU CẦU PHÊ DUYỆT]")
                print(f"👉 Hành động: {interrupt_val.get('action')}")
                print(f"👉 Thông điệp: {interrupt_val.get('message')}")
                
                choice = input("\nBạn có phê duyệt tác vụ này không? (y: Có / n: Không): ").strip().lower()

                if choice in ["y", "yes", "có", "ok"]:
                    decision_val = "yes"
                    feedback_val = "Đã phê duyệt qua CLI"
                else:
                    decision_val = "no"
                    feedback_val = input("Nhập lý do từ chối: ").strip()
                events_resume = list(app.stream(
                    Command(resume={
                        "confirmed": decision_val,
                        "feedback": feedback_val
                    }), 
                    config
                ))
        
        # 4. In câu trả lời cuối cùng từ LLM của hệ thống
        final_state = app.get_state(config)
        ai_response = final_state.values.get("response")
        if ai_response:
            print(f"AI: {ai_response}")
            
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()