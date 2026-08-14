from ..state import State


def fallback_summary_node(state: State):
    """
    Node tóm tắt dự phòng (Fallback Node): Dùng thuật toán trích xuất câu chính 
    (Rule-based Heuristic Summarizer) đảm bảo hệ thống không bao giờ trả về lỗi cho người dùng.
    """
    content = state.get("article_content", "")
    print("[FALLBACK] Đã kích hoạt Heuristic Summarizer dự phòng!")

    sentences = [s.strip() for s in content.split(".") if s.strip()]
    if sentences:
        fallback_summary = "Tóm tắt dự phòng:\n- " + "\n- ".join(sentences[:3])
    else:
        fallback_summary = "Tóm tắt dự phòng: Dữ liệu quá ngắn."

    return {
        "summary": fallback_summary,
        "used_model": "Heuristic Summarizer (Fallback)",
        "status": "FALLBACK_USED",
        "logs": ["[FALLBACK] Đã tóm tắt thành công bằng phương án dự phòng."],
        "error": None,
    }

