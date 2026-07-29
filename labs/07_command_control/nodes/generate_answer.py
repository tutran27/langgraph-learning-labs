from shared.models import GroqLLMModel

def generate_answer(state) -> dict:
    """
    Node cuối cùng để tổng hợp câu trả lời cho người dùng.
    """
    query = state.get("query", "")
    query_result = state.get("query_result", "")
    error_message = state.get("error_message", "")
    
    llm = GroqLLMModel()
    
    if query_result:
        # Trường hợp thành công: dịch kết quả thô thành câu trả lời tự nhiên
        prompt = f"""
        Bạn là trợ lý AI thông tin. Hãy dịch kết quả truy vấn database thô sau đây thành câu trả lời tự nhiên, thân thiện cho người dùng tương ứng với câu hỏi gốc của họ.
        Yêu cầu của người dùng: {query}
        Kết quả database thô: {query_result}
        
        Trả về câu trả lời tự nhiên trực tiếp, ngắn gọn và không kèm định dạng hay giải thích gì thêm.
        """
        response = llm.invoke(prompt).content.strip()
    else:
        # Trường hợp thất bại: báo lỗi thân thiện
        response = f"Xin lỗi, tôi đã thử thực thi và sửa lỗi nhưng câu lệnh SQL vẫn thất bại. Chi tiết lỗi: {error_message}"
        
    return {
        "response": response,
        "logs": [f"Generated final response: {response}"]
    }
