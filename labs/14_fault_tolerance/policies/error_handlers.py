from ..state import State


def route_after_summary(state: State) -> str:
    """
    Hàm điều hướng (Conditional Routing): 
    Nếu bước tóm tắt chính bị lỗi hoặc rỗng -> Chuyển sang Fallback Node.
    """
    if state.get("error") or not state.get("summary"):
        return "fallback_summary"
    return "END"
