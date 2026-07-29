from typing import Literal
from langgraph.types import Command

from shared.models import GroqLLMModel

def clean_sql(text: str) -> str:
    text = text.strip()
    if "```sql" in text:
        text = text.split("```sql")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return text.strip()

def sql_corrector(state) -> Command[Literal["execute_sql"]]:
    query = state.get("query", "")
    llm = GroqLLMModel()
    retry_count = state.get("retry_count", 0)
    error_message = state.get("error_message", "")
    generated_sql = state.get("generated_sql", "")

    prompt = f"""
    Bạn là một chuyên gia sửa lỗi cú pháp SQL. 
    Dưới đây là một câu lệnh SQL bị lỗi cú pháp khi thực thi. Hãy sửa lại cho đúng cú pháp chuẩn SQL.
    Đảm bảo câu lệnh SQL đúng cú pháp, đủ yêu cầu của người dùng.
    Đừng thêm bất kì ký tự nào khác ngoài câu lệnh SQL.
    Chỉ trả về câu lệnh SQL mới đã được sửa, đảm bảo phản hồi của bạn chỉ là câu lệnh, không có string hay text hay markdown thừa.
    Hãy thêm dấu ";" vào cuối câu lệnh.

    Yêu cầu gốc của người dùng: {query}
    SQL lỗi hiện tại: {generated_sql}
    Lỗi cú pháp phát hiện: {error_message}
    """
    generated_sql = llm.invoke(prompt)
    sql_code = clean_sql(generated_sql.content)
    return Command(
        update={
            "generated_sql": sql_code,
            "logs": [f"Syntax correction (Retry #{retry_count}): {sql_code}"]
        },
        goto="execute_sql"
    )

if __name__ == "__main__":
    query="Tôi muốn tạo bảng có tên Users với các cột: id, name, email, age, gender"
    sql_code="SELECTT * FROM users;"
    response=sql_corrector(
        {
            "query": query, 
            "retry_count": 1, 
            "error_message": "SQL Error: near 'SELECTT': syntax error", 
            "generated_sql": sql_code
        }
    )
    print(f"SQL Code: \n {response.update['generated_sql']}")