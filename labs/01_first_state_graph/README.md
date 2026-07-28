# Lab 01 · First State Graph

> 🕸️ Nền tảng để làm quen với StateGraph, Node, Edge và các bước thiết lập luồng chạy tuần tự trong LangGraph.

## 🎯 Mục tiêu

- Định nghĩa trạng thái (`GraphState`) sử dụng `TypedDict`.
- Triển khai logic xử lý cho từng node (Format text, Summarize và Q&A).
- Lắp ghép, kết nối các node tuần tự và biên dịch (`compile`) đồ thị.
- Kiểm thử luồng chạy (`invoke`) và viết test tự động sử dụng `pytest` với mock LLM.

## 📂 Nội dung hiện có

| File | Mô tả | Cách chạy |
| --- | --- | --- |
| `state.py` | Định nghĩa cấu trúc dữ liệu `GraphState` xuyên suốt đồ thị | - |
| `nodes.py` | Cài đặt logic cho 3 nodes: format conversation, tóm tắt và hỏi đáp | - |
| `graph.py` | Xây dựng đồ thị tuyến tính bằng `StateGraph` và biên dịch | - |
| `run.py` | Script khởi chạy giả lập dữ liệu và thực thi đồ thị | `python -m labs.01_first_state_graph.run` |
| `tests/conftest.py` | Cấu hình `sys.path` tự động cho môi trường chạy test | - |
| `tests/test_nodes.py` | Unit test cho từng nodes sử dụng mock LLM | `python -m pytest labs/01_first_state_graph/tests` |
| `tests/test_graph.py` | Integration test cho luồng chạy của toàn bộ đồ thị | `python -m pytest labs/01_first_state_graph/tests` |
