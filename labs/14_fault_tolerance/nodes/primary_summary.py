from shared.models import GroqLLMModel
from ..state import State


def primary_summary_node(state: State):
    """
    Node tóm tắt bài viết bằng Groq LLM chính (Primary LLM).
    """
    content = state.get("article_content", "")
    if not content:
        return {
            "error": "Không có nội dung bài viết để tóm tắt!",
            "logs": ["[ERROR] [PRIMARY] Bài viết rỗng."],
        }

    try:
        llm = GroqLLMModel()
        prompt = f"Hãy tóm tắt ngắn gọn 2-3 ý chính của bài viết sau dưới dạng gạch đầu dòng:\n{content}"
        res = llm.invoke(prompt)

        return {
            "summary": res.content,
            "used_model": "GroqLLM (Primary)",
            "status": "SUCCESS",
            "logs": ["[OK] [PRIMARY] Tóm tắt thành công bằng Groq LLM."],
            "error": None,
        }
    except Exception as e:
        print(f"[WARNING] [PRIMARY ERROR]: {e}")
        return {
            "error": str(e),
            "logs": [f"[WARNING] [PRIMARY ERROR] Gặp sự cố: {e}"],
        }

