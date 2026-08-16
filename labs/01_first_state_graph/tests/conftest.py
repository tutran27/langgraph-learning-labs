import sys
from pathlib import Path

# Tự động thêm thư mục gốc của Lab 1 vào PYTHONPATH khi chạy test
lab_dir = str(Path(__file__).parent.parent)
if lab_dir not in sys.path:
    sys.path.insert(0, lab_dir)
