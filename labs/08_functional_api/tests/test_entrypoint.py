import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
lab_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(lab_dir)

sys.path.insert(0, lab_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from workflow import content_generation_workflow
from langgraph.types import Command

def test_workflow_execution():
    config = {"configurable": {"thread_id": "test-thread-unique"}}
    
    # 1. Chạy lượt đầu: phải nhận được interrupt
    result1 = content_generation_workflow.invoke("Cybersecurity", config=config)
    assert "__interrupt__" in result1
    
    topic = result1["__interrupt__"][0].value["topic"]
    
    # 2. Resume lượt hai: phải hoàn tất và trả về kết quả cuối cùng
    result2 = content_generation_workflow.invoke(Command(resume="Approved"), config=config)
    
    assert "topic" in result2
    assert "draft" in result2
    assert "review" in result2
    assert "user_response" in result2
    
    assert result2["user_response"] == "Approved"
    assert result2["topic"] == topic
    assert topic in result2["draft"]
    assert result2["draft"] in result2["review"]
