# Lab 14 · Fault Tolerance & Resilience

> Xây dựng hệ thống AI Agent có khả năng chịu lỗi và tự phục hồi (Self-healing) ứng dụng trong bài toán **AI Research & Article Summarizer Assistant**. Lab này minh họa cách kết hợp `RetryPolicy`, `TimeoutPolicy`, `Conditional Fallback Routing` và xử lý ngoại lệ thực tế.

## Mục tiêu

- Sử dụng `RetryPolicy` để tự động thử lại các thao tác bị lỗi mạng/API chập chờn.
- Đặt trần thời gian thực thi `TimeoutPolicy` cho các `async` node.
- Xây dựng luồng `Fallback Node` dự phòng (Heuristic Summarizer) đảm bảo ứng dụng không bao giờ bị sập đối với người dùng.
- Phân tách kiến trúc sạch giữa `state.py`, `policies/`, `nodes/` và `graph.py`.

## Cấu trúc thư mục

- **`state.py`**: Định nghĩa `State` theo dõi URL, nội dung bài viết, kết quả tóm tắt, model đã dùng và nhật ký `logs`.
- **`policies/`**: 
  - `retries.py`: Cấu hình `RetryPolicy` (max 3 lần, backoff factor 2.0).
  - `timeouts.py`: Khai báo hằng số timeout cho tác vụ async.
  - `error_handlers.py`: Hàm điều hướng router chuyển sang Fallback khi gặp sự cố.
- **`nodes/`**:
  - `fetch_article.py`: Tải dữ liệu bài viết (async & timeout support).
  - `primary_summary.py`: Tóm tắt bài viết bằng Groq LLM thực tế.
  - `fallback_summary.py`: Tóm tắt dự phòng bằng thuật toán Heuristic Rule-based khi LLM chính lỗi.
- **`graph.py`**: Ghép nối workflow hoàn chỉnh và kiểm thử thực thi.

## Hướng dẫn chạy

Chạy trực tiếp module graph:
```bash
python -m labs.14_fault_tolerance.graph
```

Chạy bộ test suite bằng pytest:
```bash
python -m pytest labs/14_fault_tolerance/tests -v
```
