from typing import TypedDict, List, Annotated
import operator

class SQLAgentState(TypedDict):
    query: str                # Câu hỏi gốc của người dùng
    generated_sql: str        # Câu lệnh SQL hiện tại đang thử nghiệm
    query_result: str         # Kết quả trả về từ database (nếu chạy được)
    error_message: str        # Thông báo lỗi nếu chạy SQL thất bại
    retry_count: int          # Đếm số lần tự động sửa lỗi
    logs: Annotated[List[str], operator.add]  # Lịch sử logs
    response: str             # Câu trả lời cuối cùng cho người dùng
