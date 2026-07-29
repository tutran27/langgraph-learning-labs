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

def generate_sql(state) -> Command[Literal["execute_sql"]]:
    query = state.get("query", "")
    generated_sql = state.get("generated_sql", "")
    
    # Nếu câu lệnh SQL nháp đã được truyền sẵn từ đầu vào, bỏ qua sinh LLM và đi thẳng tới execute_sql
    if generated_sql:
        return Command(
            update={
                "logs": [f"Provided draft SQL: {generated_sql}"]
            },
            goto="execute_sql"
        )
        
    llm = GroqLLMModel()

    prompt = f"""
    Bạn là một chuyên gia SQL. Dựa vào yêu cầu người dùng hãy tạo câu lệnh SQL đáp ứng yêu cầu trên.
    Đảm bảo câu lệnh SQL đúng cú pháp, đủ yêu cầu của người dùng.
    Đừng thêm bất kì ký tự nào khác ngoài câu lệnh SQL.
    Chỉ trả về câu lệnh SQL, đảm bảo phản hồi của bạn chỉ là câu lệnh, không có string hay text hay markdown thừa.
    Chú ý sau mỗi câu lệnh SQL phải thêm dấu ";"
    Yêu cầu: {query}
    """
    generated_sql_resp = llm.invoke(prompt)
    sql_code = clean_sql(generated_sql_resp.content)
    return Command(
        update={
            "generated_sql": sql_code,
            "logs": [f"Generated initial draft SQL: {sql_code}"]
        },
        goto="execute_sql"
    )

if __name__ == "__main__":
    query="Tìm các thành viên có lương >= 10$/ngày trong bảng Workers"
    response=generate_sql({"query": query})
    print(f"SQL Code: \n {response.update["generated_sql"]}")