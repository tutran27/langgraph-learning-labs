from langgraph.store.memory import InMemoryStore


def create_memory_store() -> InMemoryStore:
    """
    Khởi tạo và trả về đối tượng InMemoryStore dùng chung cho ứng dụng.
    """
    return InMemoryStore()
