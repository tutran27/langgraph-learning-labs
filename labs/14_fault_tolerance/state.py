from typing import TypedDict, Optional, List, Annotated
import operator


class State(TypedDict):
    """
    Trạng thái theo dõi luồng tóm tắt bài viết thực tế có xử lý sự cố.
    """
    url_or_text: str
    article_content: str
    summary: str
    used_model: str
    error: Optional[str]
    status: str
    logs: Annotated[List[str], operator.add]
