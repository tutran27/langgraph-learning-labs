import sys
import os

# Thêm thư mục lab và thư mục gốc vào path để test tìm được module
current_dir = os.path.dirname(os.path.abspath(__file__))
lab_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(lab_dir)

sys.path.insert(0, lab_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tasks import generate_topic, write_draft, review_draft

def test_generate_topic():
    # Gọi hàm thực thi gốc của task bằng cách truy cập thuộc tính .func
    result = generate_topic.func("Test Prompt")
    assert "Test Prompt" in result
    assert "Topic:" in result

def test_write_draft():
    result = write_draft.func("Topic: 'AI' (ID: 123)")
    assert "Draft content for: Topic: 'AI' (ID: 123)" == result

def test_review_draft():
    result = review_draft.func("Draft content")
    assert "Approved draft: [ Draft content ]" == result
