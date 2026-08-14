def get_user_memory_namespace(user_id: str) -> tuple[str, str]:
    """
    Trả về tuple namespace chuẩn để phân tách bộ nhớ theo từng user_id trong Store.
    """
    return ("memories", user_id)
