import pytest
import asyncio
from langgraph.graph import StateGraph, START, END
from langgraph.errors import NodeTimeoutError

from ..state import State


@pytest.mark.asyncio
async def test_fetch_node_timeout():
    """
    Test TimeoutPolicy: Nếu node async vượt quá thời gian timeout cho phép -> Ném NodeTimeoutError.
    """
    async def slow_fetch_node(state: State):
        await asyncio.sleep(5.0)
        return {"article_content": "Late content"}

    builder = StateGraph(State)
    builder.add_node("fetch_article", slow_fetch_node, timeout=1.0)
    builder.add_edge(START, "fetch_article")
    builder.add_edge("fetch_article", END)

    app = builder.compile()

    state = {
        "url_or_text": "https://example.com",
        "article_content": "",
        "summary": "",
        "used_model": "",
        "error": None,
        "status": "PENDING",
        "logs": [],
    }

    with pytest.raises(NodeTimeoutError):
        await app.ainvoke(state)
