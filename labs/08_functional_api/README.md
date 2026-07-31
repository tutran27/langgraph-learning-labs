# Lab 8: LangGraph Functional API & Replay Cache

Lab này hướng dẫn cách sử dụng **Functional API** trong LangGraph — phương thức xây dựng chatbot/workflow dạng imperative (tuần tự) thay thế cho việc định nghĩa `StateGraph` truyền thống.

## 🎯 Mục tiêu bài học
- Học cách định nghĩa quy trình làm việc dạng hàm tuần tự thay vì vẽ đồ thị trạng thái.
- Tích hợp con người vào vòng lặp (Human-in-the-loop) với cơ chế tạm dừng (`interrupt`) và tiếp tục (`Command`).
- Tìm hiểu cơ chế **Replay Cache** tự động lưu trữ kết quả để tránh tính toán lại khi tiếp tục workflow.

---

## 🔑 Các khái niệm cốt lõi

*   **Functional API**: Thay vì định nghĩa các node và cạnh nối (edges) thủ công, ta viết code Python tuần tự giống như một hàm thông thường. LangGraph sẽ tự động xây dựng đồ thị phía dưới.
*   **Hàm `@entrypoint`**: Đóng vai trò là điểm bắt đầu và quản lý luồng chính của workflow, hỗ trợ liên kết với bộ lưu trữ checkpoint để quản lý trạng thái.
*   **Hàm `@task`**: Đại diện cho các tác vụ xử lý độc lập (tương ứng với các node). Khi gọi một task, nó trả về một đối tượng `Future`, và ta dùng `.result()` để lấy giá trị thực tế sau khi task chạy xong.
*   **Cơ chế Interrupt**: Hàm `interrupt()` được sử dụng để tạm dừng luồng chạy ngay lập tức và gửi yêu cầu phản hồi ra bên ngoài.
*   **Lệnh Command**: Lớp `Command(resume=...)` được truyền vào khi gọi `invoke` lượt tiếp theo để cung cấp dữ liệu đầu vào cần thiết để chạy tiếp luồng bị ngắt.
*   **Replay Cache**: Cơ chế tự động ghi nhớ và tái sử dụng kết quả của các tác vụ đã hoàn thành trước khi bị ngắt. Khi khôi phục đồ thị, các tác vụ này sẽ lấy trực tiếp kết quả từ cache thay vì chạy lại, đặc biệt hữu ích với các tác vụ không xác định (như sinh số ngẫu nhiên hoặc gọi API).

---

## 📁 Cấu trúc thư mục Lab 8
- [workflow.py](file:///d:/AI_LABs/langgraph-learning-labs/labs/08_functional_api/workflow.py): Định nghĩa quy trình bằng Functional API với `@entrypoint`.
- [tasks.py](file:///d:/AI_LABs/langgraph-learning-labs/labs/08_functional_api/tasks.py): Các tác vụ con (`generate_topic`, `write_draft`, `review_draft`) được bọc bởi `@task`.
- [run.py](file:///d:/AI_LABs/langgraph-learning-labs/labs/08_functional_api/run.py): Script thực hiện chạy thử nghiệm kịch bản ngắt luồng và cho phép người dùng nhập phản hồi để tiếp tục.
- `tests/`: Bộ kiểm thử tự động xác thực tính đúng đắn và tính năng Replay Cache.

---

## 🚀 Cách chạy thử nghiệm
1. Chạy chương trình và nhập phản hồi phê duyệt trực tiếp trên console:
   ```bash
   python labs/08_functional_api/run.py
   ```
2. Thực hiện kiểm thử tự động với `pytest`:
   ```bash
   pytest labs/08_functional_api/tests/
   ```
