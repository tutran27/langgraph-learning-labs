from state import OverallState

def aggregate_node(state: OverallState):
    analyses = state.get("analyses", [])
    print(f"  --> [Aggregate] Collecting and sorting {len(analyses)} worker analyses...")
    
    sorted_analyses = sorted(analyses, key=lambda x: x.get("chunk_id", 0))
    
    lines = [
        "=== BÁO CÁO PHÂN TÍCH VĂN BẢN TỔNG HỢP (MAP-REDUCE) ===",
        f"Tổng số đoạn đã xử lý: {len(sorted_analyses)}\n"
    ]
    
    for item in sorted_analyses:
        chunk_id = item.get("chunk_id", "?")
        summary = item.get("summary", "")
        lines.append(f"📌 [Đoạn #{chunk_id}]: {summary}")
        
    lines.append("\n===> TỔNG KẾT: Hoàn thành phân tích toàn bộ tài liệu.")
    final_text = "\n".join(lines)
    return {"final_report": final_text}
