from typing import TypedDict, Optional

class ApprovalState(TypedDict):
    query: str                 # Câu chat đầu vào của người dùng
    action: str                # Hành động nhạy cảm trích xuất được (nếu có, ví dụ: "gửi email")
    approved: Optional[bool]   # Trạng thái duyệt: True (Đồng ý), False (Từ chối), None (Chờ quyết định)
    feedback: Optional[str]    # Lời nhắn hoặc lý do từ chối từ người duyệt
    response: Optional[str]    # Câu trả lời cuối cùng từ hệ thống hiển thị cho user
