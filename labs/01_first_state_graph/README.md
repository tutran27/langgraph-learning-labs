# Lab 01 · First State Graph

> 🕸️ Nền tảng làm quen với StateGraph, Node, Edge và luồng chạy tuần tự trong LangGraph.

## 🎯 Mục tiêu

- Định nghĩa trạng thái (`GraphState`) sử dụng `TypedDict`.
- Triển khai logic xử lý cho từng node (Format, Summarize, Q&A).
- Lắp ghép node tuần tự, biên dịch (`compile`) và chạy đồ thị (`invoke`).
- Viết test tự động với `pytest` + mock LLM.

## 📂 Cấu trúc & Ý tưởng (Text Processing Pipeline)

- **`state.py`**: Định nghĩa `GraphState` xuyên suốt đồ thị.
- **`nodes.py`**: Logic 3 nodes: format conversation, tóm tắt, hỏi đáp.
- **`graph.py`**: Xây dựng đồ thị tuyến tính bằng `StateGraph`.
- **`run.py`**: Script khởi chạy giả lập dữ liệu và thực thi đồ thị.

## ⚙️ Hướng dẫn khởi chạy

```bash
python -m labs.01_first_state_graph.run
```

```bash
python -m pytest labs/01_first_state_graph/tests -v
```
