import sys
import os

# Thêm thư mục hiện tại và thư mục gốc dự án vào PYTHONPATH để tránh lỗi import
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))

sys.path.insert(0, current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from graph import graph

def run_test_cases():
    print("====================================================")
    print("=== CHAY THU NGHIEM SQL AUTO-CORRECTION AGENT (LAB 7) ===")
    print("====================================================\n")

    # Kịch bản 1: Sai tên bảng (Tự động sửa từ 'employee' thành 'users')
    print("--- Kịch bản 1: Sửa tên bảng (Schema Explorer) ---")
    state_1 = {
        "query": "Lấy danh sách người dùng trong bảng employee",
        "generated_sql": "",
        "query_result": "",
        "error_message": "",
        "retry_count": 0,
        "logs": [],
        "response": ""
    }

    config={
    "configurable": {
        "thread_id": "thread_1"
    }
}

    result_1 = graph.invoke(state_1, config=config)
    print(f"Câu hỏi: {state_1['query']}")
    print("Lịch trình thực thi của Graph (Logs):")
    for log in result_1["logs"]:
        print(f"  - {log}")
    print(f"Kết quả SQL cuối cùng: {result_1['generated_sql']}")
    print(f"Câu trả lời cuối cùng: {result_1['response']}")
    print("\n----------------------------------------------------\n")

    # Kịch bản 2: Sai cú pháp SQL (Sửa từ khóa SELECTT -> SELECT)
    print("--- Kịch bản 2: Sửa lỗi cú pháp (Syntax Corrector) ---")
    state_2 = {
        "query": "Lấy thông tin người dùng",
        "generated_sql": "SELECTT * FROM users;", # Cố tình truyền SQL lỗi từ đầu vào
        "query_result": "",
        "error_message": "",
        "retry_count": 0,
        "logs": [],
        "response": ""
    }
    result_2 = graph.invoke(state_2, config=config)
    print(f"SQL nháp ban đầu: {state_2['generated_sql']}")
    print("Lịch trình thực thi của Graph (Logs):")
    for log in result_2["logs"]:
        print(f"  - {log}")
    print(f"Kết quả SQL cuối cùng: {result_2['generated_sql']}")
    print(f"Câu trả lời cuối cùng: {result_2['response']}")
    print("====================================================")

if __name__ == "__main__":
    run_test_cases()
