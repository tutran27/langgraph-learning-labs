import pytest
from ..graph import create_resilient_summarizer_graph


@pytest.mark.asyncio
async def test_fallback_when_primary_fails(monkeypatch):
    """
    Test cơ chế Fallback: Khi Primary LLM bị lỗi -> Tự động chuyển hướng sang Heuristic Summarizer.
    """
    # Mock primary_summary_node trả về lỗi
    def mock_primary_summary_node(state):
        return {
            "error": "Groq API Limit Exceeded",
            "logs": ["[ERROR] Primary LLM failed"],
        }

    from ..nodes import primary_summary
    monkeypatch.setattr(primary_summary, "primary_summary_node", mock_primary_summary_node)

    graph = create_resilient_summarizer_graph()
    initial_state = {
        "url_or_text": "LangGraph hỗ trợ cơ chế Fallback dự phòng cho AI Agent.",
        "article_content": "",
        "summary": "",
        "used_model": "",
        "error": None,
        "status": "PENDING",
        "logs": [],
    }

    result = await graph.ainvoke(initial_state)

    assert result["status"] == "FALLBACK_USED"
    assert "Heuristic" in result["used_model"]
    assert "Tóm tắt dự phòng" in result["summary"]
