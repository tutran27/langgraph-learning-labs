import sys
import os
import io

# Force UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import graph

def main():
    print("="*60)
    print("RUNNING AUTO-REPAIR AGENT")
    print("="*60)

    initial_state = {
        "task_description": (
            "Write a Python function 'is_palindrome(s)' that returns True if the string 's' "
            "is a palindrome, and False otherwise. Important: it must be case-insensitive "
            "and ignore all spaces and special punctuation characters (like commas, periods, exclamation marks)."
        ),
        "test_cases": [
            {"input": "racecar", "expected": True},
            {"input": "Hello", "expected": False},
            {"input": "A man, a plan, a canal: Panama", "expected": True},
            {"input": "race a car", "expected": False},
            {"input": "Was it a car or a cat I saw?", "expected": True}
        ],
        "attempts": 0,
        "max_attempts": 3
    }
    
    config = {"recursion_limit": 10, "configurable": {"thread_id": "run_1"}}
    
    final_state = dict(initial_state)
    try:
        for event in graph.stream(initial_state, config=config):
            for node_name, state_update in event.items():
                final_state.update(state_update)
                print(f"\n>>> [Nút Hoàn Thành] {node_name} <<<")
                
                if "code" in state_update:
                    print("--- Mã nguồn được sinh ra/sửa đổi ---")
                    print(state_update["code"])
                    
                if "feedback" in state_update:
                    print(f"Phản hồi (Feedback): {state_update['feedback']}")
                    
                if "is_correct" in state_update:
                    print(f"Kết quả kiểm thử (Is Correct): {state_update['is_correct']}")
                    
                if "attempts" in state_update:
                    print(f"Số lần sửa (Attempts): {state_update['attempts']}")
                    
                if "stop_reason" in state_update:
                    print(f"Lý do dừng (Stop Reason): {state_update['stop_reason']}")
    except Exception as e:
        print(f"\n[Error] Đồ thị bị dừng đột ngột: {e}")
                
    # Xem kết quả cuối cùng trong State
    print("\n" + "="*60)
    print("KẾT QUẢ CUỐI CÙNG")
    print("="*60)
    print(f"Đúng hay sai: {final_state.get('is_correct')}")
    print(f"Tổng số lần sửa: {final_state.get('attempts')}")
    print(f"Lý do dừng đồ thị: {final_state.get('stop_reason')}")
    print("\nMã nguồn hoàn chỉnh:")
    print(final_state.get('code'))
    
if __name__ == "__main__":
    main()
