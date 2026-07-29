# Lab 05 · Parallel Execution & Reducer Merge

> ⚡ Chạy song song các Node độc lập (Fan-out) và gom kết quả về một Node chung (Fan-in) với Reducer trong LangGraph.

## 🎯 Mục tiêu
- Hiểu mô hình Super-step trong LangGraph khi xử lý các node rẽ nhánh.
- Áp dụng `Annotated[list, operator.add]` để tích lũy dữ liệu trả về từ nhiều node song song mà không bị ghi đè.
- Xây dựng luồng Fan-out / Fan-in thực tế (Phân tích cổ phiếu).
- Kiểm chứng tốc độ cải thiện giữa chạy tuần tự và chạy song song.

## ⚙️ Khởi chạy

Chạy benchmark so sánh tốc độ:
```powershell
$env:PYTHONPATH="."; python labs/05_parallel_execution/benchmarks.py
```

Chạy bộ unit test tự động:
```powershell
$env:PYTHONPATH="."; pytest labs/05_parallel_execution/tests
```
