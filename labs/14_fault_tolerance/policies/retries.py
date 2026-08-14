from langgraph.types import RetryPolicy

# RetryPolicy cho API/LLM: Thử lại tối đa 3 lần nếu gặp sự cố mạng hoặc API chập chờn
llm_retry_policy = RetryPolicy(
    max_attempts=3,
    initial_interval=1.0,
    backoff_factor=2.0,
    retry_on=Exception,
)