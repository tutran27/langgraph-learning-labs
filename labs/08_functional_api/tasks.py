import random
import time
from langgraph.func import task

@task
def generate_topic(prompt: str) -> str:
    """Tạo ra chủ đề ngẫu nhiên kèm mã ID ngẫu nhiên (non-deterministic)."""
    time.sleep(1)
    random_id = random.randint(1000, 9999)
    return f"Topic: '{prompt}' (ID: {random_id})"

@task
def write_draft(topic: str) -> str:
    """Viết dự thảo bài viết dựa trên chủ đề."""
    time.sleep(1)
    return f"Draft content for: {topic}"

@task
def review_draft(draft: str) -> str:
    """Đánh giá và phê duyệt bản thảo."""
    time.sleep(1)
    return f"Approved draft: [ {draft} ]"
