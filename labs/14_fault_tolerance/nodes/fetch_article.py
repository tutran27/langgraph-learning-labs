import asyncio
from ..state import State


async def fetch_article_node(state: State):
    """
    Node thu thập nội dung bài viết (hỗ trợ Async & TimeoutPolicy).
    """
    url_or_text = state.get("url_or_text", "")

    if not url_or_text:
        return {
            "error": "Nội dung đầu vào rỗng!",
            "logs": ["[ERROR] [FETCH] Nội dung đầu vào rỗng."],
        }

    # Giả lập tải dữ liệu bài viết từ web (async)
    if url_or_text.startswith("http"):
        await asyncio.sleep(1.0)
        content = (
            f"Bài viết từ URL {url_or_text}: LangGraph 0.2+ hỗ trợ RetryPolicy, "
            f"Fallback và TimeoutPolicy giúp AI Agent hoạt động ổn định và tự phục hồi khi gặp sự cố."
        )
    else:
        content = url_or_text

    return {
        "article_content": content,
        "logs": ["[OK] [FETCH] Đã tải dữ liệu bài viết thành công."],
    }

