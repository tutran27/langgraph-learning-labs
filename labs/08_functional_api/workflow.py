from langgraph.func import entrypoint
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt
from tasks import generate_topic, write_draft, review_draft

checkpointer = InMemorySaver()

@entrypoint(checkpointer=checkpointer)
def content_generation_workflow(prompt: str) -> dict:
    """Quy trình tạo nội dung sử dụng Functional API."""
    # 1. Gọi task sinh chủ đề và đợi kết quả (.result())
    topic_future = generate_topic(prompt)
    topic = topic_future.result()
    
    # 2. Tạm dừng để xin phê duyệt chủ đề từ người dùng (Human-in-the-loop)
    user_response = interrupt({
        "question": f"Bạn có duyệt chủ đề: '{topic}'?",
        "topic": topic
    })
    
    # 3. Gọi task viết bản thảo
    draft_future = write_draft(topic)
    draft = draft_future.result()
    
    # 4. Gọi task phê duyệt
    review_future = review_draft(draft)
    final_output = review_future.result()
    
    return {
        "topic": topic,
        "draft": draft,
        "review": final_output,
        "user_response": user_response
    }
