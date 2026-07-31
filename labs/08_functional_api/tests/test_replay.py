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

def test_workflow_replay_idempotency():
    # Cấu hình thread 1
    config1 = {"configurable": {"thread_id": "test-replay-thread-1"}}
    
    # 1. Chạy lượt đầu của thread 1 -> Dừng ở interrupt, lấy topic sinh ngẫu nhiên
    res1_run1 = content_generation_workflow.invoke("Machine Learning", config=config1)
    topic1 = res1_run1["__interrupt__"][0].value["topic"]
    
    # 2. Resume thread 1 -> Đồ thị hoàn thành
    res1_run2 = content_generation_workflow.invoke(Command(resume="Yes"), config=config1)
    topic1_final = res1_run2["topic"]
    
    # Kiểm tra tính replay: sau khi resume, chủ đề từ cache không đổi
    assert topic1 == topic1_final, "Replay trên cùng một thread không bảo toàn ID ngẫu nhiên!"
    
    # 3. Chạy thread 2 (khác thread_id) -> Dừng ở interrupt, lấy topic sinh ngẫu nhiên mới
    config2 = {"configurable": {"thread_id": "test-replay-thread-2"}}
    res2_run1 = content_generation_workflow.invoke("Machine Learning", config=config2)
    topic2 = res2_run1["__interrupt__"][0].value["topic"]
    
    # Kiểm tra tính cô lập: khác thread thì ID ngẫu nhiên phải khác nhau
    assert topic1 != topic2, "Các thread khác nhau không cô lập dữ liệu ngẫu nhiên!"
