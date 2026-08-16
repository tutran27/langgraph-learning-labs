from shared.models import GroqLLMModel

from ..state import ApprovalState


def prepare_action(state: ApprovalState) -> ApprovalState:
    """LLM phân tích câu chat và trích xuất hành động nhạy cảm cần duyệt."""
    query=state.get("query")

    model=GroqLLMModel()

    classify_prompt = f"""Bạn là trợ lý giám sát hành động. Hãy phân tích yêu cầu sau của người dùng:
"{query}"
Yêu cầu này có chứa hành động thực thi nhạy cảm nào cần phê duyệt trước khi chạy không (ví dụ: chuyển tiền, gửi email, xóa dữ liệu, thực thi mã nguồn)?
- Nếu CÓ: Trích xuất hành động đó thành 1 câu ngắn gọn (ví dụ: "Gửi báo cáo doanh thu cho CEO", "Chuyển 500 USD").
- Nếu KHÔNG: Chỉ trả về đúng từ "NONE".
Hãy trả về chính xác câu trích xuất hoặc "NONE", không giải thích thêm."""

    result=model.invoke(classify_prompt).content

    if result != "NONE":
        return {"action": result}
    else:
        return {"action": None}

if __name__ == "__main__":
    query="Chuyển cho tôi 10 triệu VNĐ"
    print(prepare_action({"query": query})) 