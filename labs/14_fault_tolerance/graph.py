import asyncio
from langgraph.graph import StateGraph, START, END

from .state import State
from .policies.retries import llm_retry_policy
from .policies.timeouts import FETCH_TIMEOUT_SECONDS
from .policies.error_handlers import route_after_summary
from .nodes.fetch_article import fetch_article_node
from .nodes.primary_summary import primary_summary_node
from .nodes.fallback_summary import fallback_summary_node


def create_resilient_summarizer_graph():
    builder = StateGraph(State)

    # 1. Thêm các node với TimeoutPolicy & RetryPolicy
    builder.add_node("fetch_article", fetch_article_node, timeout=FETCH_TIMEOUT_SECONDS)
    builder.add_node("primary_summary", primary_summary_node, retry=llm_retry_policy)
    builder.add_node("fallback_summary", fallback_summary_node)

    # 2. Xây dựng luồng thực thi
    builder.add_edge(START, "fetch_article")
    builder.add_edge("fetch_article", "primary_summary")

    # 3. Conditional Edge: Nếu primary_summary bị lỗi -> Chuyển sang fallback_summary
    builder.add_conditional_edges(
        "primary_summary",
        route_after_summary,
        {
            "fallback_summary": "fallback_summary",
            "END": END,
        },
    )
    builder.add_edge("fallback_summary", END)


    return builder.compile()


async def main():
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    graph = create_resilient_summarizer_graph()
    initial_state = {
        "url_or_text": "https://langchain.com/blog/langgraph-fault-tolerance",
        "article_content": "",
        "summary": "",
        "used_model": "",
        "error": None,
        "status": "PENDING",
        "logs": [],
    }

    result = await graph.ainvoke(initial_state)

    print("\n--- KET QUA TOM TAT THUC TE (REAL RESILIENT WORKFLOW) ---")
    print(f"Status: {result.get('status')}")
    print(f"Model Used: {result.get('used_model')}")
    print(f"Summary:\n{result.get('summary')}")
    print("\n--- Lich su Log thuc thi ---")
    for log in result.get("logs", []):
        print("  ", log)


if __name__ == "__main__":
    asyncio.run(main())


