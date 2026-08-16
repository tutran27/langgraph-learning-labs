import sqlite3
from typing import Literal
from langgraph.types import Command

def execute_sql(state):
    generated_sql = state["generated_sql"]
    retry_count = state["retry_count"]

    import os
    # Lấy đường dẫn tới file database.db vật lý đã được build sẵn
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "sqlite.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor() 

    try:
        # Thực thi duy nhất 1 câu lệnh SQL
        cursor.execute(generated_sql)

        # Lấy kết quả nếu là SELECT
        if generated_sql.strip().upper().startswith("SELECT"):
            query_result = str(cursor.fetchall())
        else:
            conn.commit()
            query_result = "Successfully executed SQL"

        return Command(
            update={
                "query_result": query_result,
                "logs": [f"Executed SQL: {generated_sql}"]
            },
            goto="generate_answer"
        )
    # A. SQL lỗi không đúng cú pháp
    except sqlite3.OperationalError as e:
        error_message=f"SQL Error: {e}"
        
        if "syntax error" in error_message.lower() or "near" in error_message.lower():
            if retry_count > 3:
                return Command(
                    update={
                        "error_message": error_message,
                        "logs": [f"Syntax error: Failed SQL: {generated_sql}"]
                    },
                    goto="generate_answer"
                ) 
             
            return Command(
                update={
                    "error_message": error_message,
                    "logs": [f"Syntax error: Failed SQL: {generated_sql}"],
                    "retry_count": retry_count + 1
                },
                goto="sql_corrector"
            )

        # B. SQL lỗi thiếu bảng (table chưa tồn tại)
        elif "no such table" in error_message.lower():
            return Command(
                update={
                    "error_message": error_message,
                    "logs": [f"Table not found: {error_message}"],
                },
                goto="schema_explorer"
            ) 
        # C. SQL lỗi logic hoặc tham chiếu sai cột
        else: 
            return Command(
                update={
                    "error_message": error_message,
                    "logs": [f"Logic Error: {error_message}"],
                },
                goto="sql_corrector"
            ) 

    finally:
     
        conn.close()