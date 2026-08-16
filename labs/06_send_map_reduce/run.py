import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import graph

def main():
    sample_file = "labs/06_send_map_reduce/sample_data/BÁO CÁO TÓM TẮT ĐỀ XUẤT DỰ ÁN.pdf"
    file_name = os.path.basename(sample_file)
    
    print("=" * 60)
    print("🚀 CHẠY ĐỒ THỊ LAB 06: MAP-REDUCE & DYNAMIC FAN-OUT")
    print("=" * 60)
    print(f"File đầu vào: {file_name}\n")
    
    input_state = {
        "document_path": sample_file,
        "analyses": []
    }
    
    result = graph.invoke(input_state)
    
    print("\n" + "=" * 60)
    print("📊 KẾT QUẢ BÁO CÁO TỔNG HỢP (FINAL REPORT)")
    print("=" * 60)
    print(result.get("final_report", "Không có báo cáo."))

if __name__ == "__main__":
    main()
