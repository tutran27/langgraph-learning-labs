from nodes.execute_sql import execute_sql
from nodes.sql_corrector import sql_corrector
from nodes.schema_explorer import schema_explorer
from nodes.generate_sql import generate_sql
from unittest.mock import MagicMock, patch

@patch("nodes.generate_sql.GroqLLMModel")
def test_generate_sql_goto(mock_llm_class):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="SELECT 1;")
    mock_llm_class.return_value = mock_llm

    state = {"query": "SELECT 1;"}
    result = generate_sql(state)
    assert result.goto == "execute_sql"

def test_execute_sql_success_goto():
    state = {
        "generated_sql": "SELECT 1;",
        "retry_count": 0,
        "logs": []
    }
    result = execute_sql(state)
    assert result.goto == "generate_answer"

def test_execute_sql_syntax_error_goto():
    state = {
        "generated_sql": "SELECTT 1;",
        "retry_count": 0,
        "logs": []
    }
    result = execute_sql(state)
    assert result.goto == "sql_corrector"

def test_execute_sql_table_not_found_goto():
    state = {
        "generated_sql": "SELECT * FROM user;",
        "retry_count": 0,
        "logs": []
    }
    result = execute_sql(state)
    assert result.goto == "schema_explorer"

@patch("nodes.sql_corrector.GroqLLMModel")
def test_sql_corrector_goto(mock_llm_class):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="SELECT * FROM users;")
    mock_llm_class.return_value = mock_llm

    state = {
        "query": "SELECT * FROM users;",
        "generated_sql": "SELECTT * FROM users;",
        "error_message": "near SELECTT syntax error",
        "retry_count": 0,
        "logs": []
    }
    result = sql_corrector(state)
    assert result.goto == "execute_sql"

@patch("nodes.schema_explorer.GroqLLMModel")
def test_schema_explorer_goto(mock_llm_class):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="SELECT * FROM users;")
    mock_llm_class.return_value = mock_llm

    state = {
        "query": "SELECT * FROM users;",
        "generated_sql": "SELECT * FROM user;",
        "error_message": "no such table: user",
        "retry_count": 0,
        "logs": []
    }
    result = schema_explorer(state)
    assert result.goto == "execute_sql"
