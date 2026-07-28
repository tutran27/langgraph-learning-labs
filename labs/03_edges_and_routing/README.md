# Lab 03 · Edges and Conditional Routing

> 🕸️ Tìm hiểu cơ chế định tuyến có điều kiện (Conditional Routing) và phân phối luồng xử lý thông minh dựa trên State trong LangGraph.

## 🎯 Mục tiêu

- Hiểu và áp dụng cơ chế rẽ nhánh có điều kiện (`add_conditional_edges`).
- Sử dụng hàm Router để điều hướng luồng dữ liệu tự động theo trạng thái của State.
- Định nghĩa kiểu dữ liệu chặt chẽ cho Router bằng `Literal` để tăng tính an toàn cho luồng xử lý.
- Xử lý các trường hợp ngoại lệ và từ chối các định dạng không được hỗ trợ (unsupported/fallback).

## 📂 Cấu trúc & Ý tưởng (DevOps Alert & Log Analyzer)

Bài Lab này giả lập một cổng tiếp nhận thông tin giám sát DevOps:
- **`state.py`**: Định nghĩa `RouterState` gồm `input_data`, `input_type`, `processed_result` và lý do rẽ nhánh `routing_reason`.
- **`nodes/classify.py`**: Tự động nhận diện dữ liệu: chuỗi chữ làm log văn bản (`text`), số nguyên/thực làm mã trạng thái HTTP (`number`), các kiểu dữ liệu khác là không hỗ trợ (`unsupported`).
- **`nodes/process_text.py`**: Phân tích từ khóa khẩn cấp trong Log.
- **`nodes/process_number.py`**: Tra cứu mã trạng thái HTTP (200, 404, 500, 503, ...).
- **`nodes/reject.py`**: Thông báo từ chối nhận các định dạng lỗi.
- **`routers.py`**: Định nghĩa hàm định tuyến `route_input` dẫn đường cho đồ thị.
- **`graph.py`**: Xây dựng đồ thị `StateGraph` và thiết lập `add_conditional_edges`.
- **`run_cases.py`**: Script chạy thực nghiệm để theo dõi hành vi định tuyến trực quan.

## ⚙️ Hướng dẫn khởi chạy

Chạy kiểm thử các trường hợp dữ liệu mẫu:
```bash
python -m labs.03_edges_and_routing.run_cases
```

Chạy bộ unit test tự động:
```bash
python -m pytest labs/03_edges_and_routing/tests
```
