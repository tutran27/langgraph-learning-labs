from nodes.execute_sql import execute_sql
from langgraph.types import Command

def test_execute_sql_success_updates():
    # Test khi chạy SQL thành công
    state = {
        "generated_sql": "SELECT 1;",
        "retry_count": 0,
        "logs": []
    }
    result = execute_sql(state)
    
    assert isinstance(result, Command)
    assert result.update["query_result"] == "Successfully executed SQL"
    assert "Executed SQL" in result.update["logs"][0]

def test_execute_sql_syntax_error_updates():
    # Test khi chạy SQL lỗi cú pháp (near SELECTT)
    state = {
        "generated_sql": "SELECTT 1;",
        "retry_count": 1,
        "logs": []
    }
    result = execute_sql(state)
    
    assert isinstance(result, Command)
    assert "SQL Error" in result.update["error_message"]
    assert result.update["retry_count"] == 2
    assert "Syntax error" in result.update["logs"][0]

def test_execute_sql_table_not_found_updates():
    # Test khi chạy SQL lỗi sai tên bảng
    state = {
        "generated_sql": "SELECT * FROM user;",
        "retry_count": 0,
        "logs": []
    }
    result = execute_sql(state)
    
    assert isinstance(result, Command)
    assert "SQL Error: no such table" in result.update["error_message"]
    assert "Table not found" in result.update["logs"][0]
