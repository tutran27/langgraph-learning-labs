import os
import sqlite3
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

def schema_explorer(state) -> Command[Literal["execute_sql"]]:
    query = state.get("query", "")
    llm = GroqLLMModel()
    retry_count = state.get("retry_count", 0)
    error_message = state.get("error_message", "")
    generated_sql = state.get("generated_sql", "")

    # 1. TRUY VẤN ĐỘNG: Lấy danh sách bảng thực tế từ sqlite.db
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "sqlite.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query lấy tên các bảng đang tồn tại trong SQLite (bỏ qua hệ thống sqlite_%)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    existing_tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    # Chuyển mảng bảng thành chuỗi: e.g. "users, employees, products"
    schema_catalog_str = ", ".join(existing_tables) if existing_tables else "Chưa có bảng nào"

    # 2. BƠM DỮ LIỆU ĐỘNG VÀO PROMPT
    prompt = f"""
    Bạn là một chuyên gia cơ sở dữ liệu và Schema Catalog.
    Dưới đây là một câu lệnh SQL bị lỗi tham chiếu đối tượng (sai tên bảng hoặc sai tên cột).
    
    Hãy đối chiếu với danh sách các bảng THỰC TẾ đang có trong Database hiện tại để sửa lỗi:
    - Danh sách bảng đang tồn tại: {schema_catalog_str}
    
    Nguyên tắc xử lý:
    1. Nếu bảng mà người dùng muốn truy vấn đã tồn tại trong danh sách [{schema_catalog_str}], hãy sửa lại câu lệnh SQL cho đúng tên bảng đó.
    2. Nếu bảng mà người dùng muốn truy vấn KHÔNG có trong danh sách [{schema_catalog_str}] (ví dụ: một bảng hoàn toàn mới):
       - Bạn phải tự động sinh thêm câu lệnh `CREATE TABLE <tên_bảng> (...)` với các cột phù hợp để tạo bảng đó trước câu lệnh truy vấn chính.
       - Hãy đặt câu lệnh `CREATE TABLE` trước và câu lệnh truy vấn sau, ngăn cách nhau bằng dấu chấm phẩy (;).
       - Ví dụ: "CREATE TABLE Workers (id INT PRIMARY KEY, name TEXT, salary REAL); SELECT * FROM Workers;"
       
    Đảm bảo câu lệnh SQL đúng cấu trúc. Chỉ trả về mã SQL, không viết chữ giải thích hay markdown code block thừa.
    Hãy thêm dấu ";" vào cuối mỗi câu lệnh.

    Yêu cầu gốc của người dùng: {query}
    SQL lỗi hiện tại: {generated_sql}
    Lỗi từ database báo về: {error_message}
    """
    
    generated_sql_resp = llm.invoke(prompt)
    sql_code = clean_sql(generated_sql_resp.content)
    return Command(
        update={
            "generated_sql": sql_code,
            "logs": [f"Schema explorer correction (Retry #{retry_count}): {sql_code}"]
        },
        goto="execute_sql"
    )

if __name__ == "__main__":
    query="Lấy toàn bộ thông tin người dùng"
    sql_code="SELECT * FROM user;" # Sai bảng 'user' thay vì 'users'
    response=schema_explorer(
        {
            "query": query, 
            "retry_count": 1, 
            "error_message": "SQL Error: no such table: user", 
            "generated_sql": sql_code
        }
    )
    print(f"SQL Code: \n {response.update['generated_sql']}")