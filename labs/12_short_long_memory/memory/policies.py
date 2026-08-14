DEFAULT_MEMORY_SEARCH_LIMIT = 5


def should_save_memory(should_save: bool, summary: str) -> bool:
    """
    Chính sách kiểm tra điều kiện ghi nhớ:
    Phải có cờ should_save=True và chuỗi summary có nội dung hợp lệ.
    """
    if not should_save:
        return False
    if not summary or not isinstance(summary, str) or not summary.strip():
        return False
    return True
