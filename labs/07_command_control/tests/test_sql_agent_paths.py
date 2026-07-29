from unittest.mock import MagicMock, patch
from graph import graph

@patch("shared.models.GroqLLMModel")
def test_sql_agent_success_path(mock_llm_class):
    # Mock LLM trả về SQL chuẩn ngay từ đầu
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = [
        MagicMock(content="SELECT * FROM users;"),  # generate_sql
        MagicMock(content="Đây là danh sách người dùng.")  # generate_answer
    ]
    mock_llm_class.return_value = mock_llm

    initial_state = {
        "query": "Lấy thông tin người dùng",
        "generated_sql": "",
        "query_result": "",
        "error_message": "",
        "retry_count": 0,
        "logs": [],
        "response": ""
    }

    final_state = graph.invoke(initial_state)

    assert final_state["query_result"] == "Successfully executed SQL"
    assert final_state["response"] == "Đây là danh sách người dùng."
    assert any("Executed SQL: SELECT * FROM users;" in log for log in final_state["logs"])


@patch("shared.models.GroqLLMModel")
def test_sql_agent_syntax_correction_path(mock_llm_class):
    # Mock LLM trả về SQL lỗi cú pháp -> sửa cú pháp -> thành công
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = [
        MagicMock(content="SELECTT * FROM users;"),  # generate_sql (Lỗi SELECTT)
        MagicMock(content="SELECT * FROM users;"),   # sql_corrector (Đã sửa lỗi)
        MagicMock(content="Thành viên gồm Alice và Bob.")  # generate_answer
    ]
    mock_llm_class.return_value = mock_llm

    initial_state = {
        "query": "Lấy thông tin người dùng",
        "generated_sql": "",
        "query_result": "",
        "error_message": "",
        "retry_count": 0,
        "logs": [],
        "response": ""
    }

    final_state = graph.invoke(initial_state)

    assert final_state["query_result"] == "Successfully executed SQL"
    assert final_state["response"] == "Thành viên gồm Alice và Bob."
    assert any("Syntax error" in log for log in final_state["logs"])
    assert any("Syntax correction" in log for log in final_state["logs"])


@patch("shared.models.GroqLLMModel")
def test_sql_agent_table_name_correction_path(mock_llm_class):
    # Mock LLM trả về sai bảng user -> sửa thành users -> thành công
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = [
        MagicMock(content="SELECT * FROM user;"),    # generate_sql (Sai bảng user)
        MagicMock(content="SELECT * FROM users;"),   # schema_explorer (Đã sửa sang users)
        MagicMock(content="Thông tin người dùng hợp lệ.") # generate_answer
    ]
    mock_llm_class.return_value = mock_llm

    initial_state = {
        "query": "Lấy thông tin người dùng",
        "generated_sql": "",
        "query_result": "",
        "error_message": "",
        "retry_count": 0,
        "logs": [],
        "response": ""
    }

    final_state = graph.invoke(initial_state)

    assert final_state["query_result"] == "Successfully executed SQL"
    assert final_state["response"] == "Thông tin người dùng hợp lệ."
    assert any("Table not found" in log for log in final_state["logs"])
    assert any("Schema explorer correction" in log for log in final_state["logs"])


@patch("shared.models.GroqLLMModel")
def test_sql_agent_max_retry_failure_path(mock_llm_class):
    # Mock LLM sinh ra lỗi cú pháp liên tục và không thể tự sửa
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = [
        MagicMock(content="SELECTT * FROM users;"),  # generate_sql
        MagicMock(content="SELECTT * FROM users;"),  # sql_corrector (Thử lại 1)
        MagicMock(content="SELECTT * FROM users;"),  # sql_corrector (Thử lại 2)
        MagicMock(content="SELECTT * FROM users;"),  # sql_corrector (Thử lại 3)
        MagicMock(content="SELECTT * FROM users;"),  # sql_corrector (Thử lại 4)
    ]
    mock_llm_class.return_value = mock_llm

    initial_state = {
        "query": "Lấy thông tin người dùng",
        "generated_sql": "",
        "query_result": "",
        "error_message": "",
        "retry_count": 0,
        "logs": [],
        "response": ""
    }

    final_state = graph.invoke(initial_state)

    # Đảm bảo đã chạy hết số lần thử tối đa, dừng lại và xuất thông báo lỗi
    assert final_state["query_result"] == ""
    assert "SQL Error" in final_state["error_message"]
    assert "Xin lỗi" in final_state["response"]
    assert any("Failed SQL" in log for log in final_state["logs"])
