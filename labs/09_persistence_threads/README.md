# Lab 9: Persistence, Threads và Checkpoints trong LangGraph

Lab này hướng dẫn cách cấu hình lưu trữ trạng thái (Persistence) cho đồ thị hội thoại (Graph API) sử dụng các Checkpointer khác nhau (InMemory và SQLite), đồng thời tìm hiểu tính cô lập luồng (Thread Isolation) và cách truy vấn lịch sử trạng thái.

## 🎯 Mục tiêu bài học
- Hiểu nguyên lý lưu trữ trạng thái của LangGraph thông qua **Checkpointer**.
- Phân biệt sự khác nhau giữa **InMemorySaver** (Bộ nhớ tạm RAM) và **SqliteSaver** (Bộ nhớ bền vững SQLite).
- Kiểm chứng tính cô lập dữ liệu giữa các luồng hội thoại khác nhau bằng **`thread_id`**.
- Học cách truy vấn trạng thái hiện tại (`get_state`) và lịch sử các bước chạy (`get_state_history`) của một thread.

---

## 🔑 Các khái niệm cốt lõi

*   **Checkpointer**: Thành phần chịu trách nhiệm lưu trữ và phục hồi trạng thái (State) của đồ thị sau mỗi bước chạy hoặc khi kết thúc mỗi lượt chạy (`invoke`).
*   **InMemorySaver**: Lưu dữ liệu trực tiếp trên RAM của tiến trình Python đang chạy. Dữ liệu sẽ biến mất ngay khi tiến trình kết thúc. Phù hợp cho kiểm thử nhanh.
*   **SqliteSaver**: Lưu dữ liệu vào file cơ sở dữ liệu SQLite cục bộ (ví dụ `state.db`). Trạng thái được bảo toàn kể cả khi tiến trình Python bị tắt đi và khởi động lại.
*   **Thread ID (`thread_id`)**: Mã định danh luồng hội thoại. LangGraph sử dụng `thread_id` trong cấu hình để phân tách dữ liệu của các cuộc hội thoại khác nhau, đảm bảo người dùng này không đọc được lịch sử chat của người dùng khác (**Thread Isolation**).
*   **State Snapshot**: Bản sao lưu trạng thái tại một thời điểm, chứa các thuộc tính quan trọng:
    *   `values`: Giá trị thực tế của State (danh sách messages, query...).
    *   `config`: Chứa cấu hình và mã định danh checkpoint cụ thể (`checkpoint_id`).
    *   `next`: Tên node chuẩn bị chạy tiếp theo (rỗng `()` nếu đồ thị đã chạy xong).
    *   `metadata`: Siêu dữ liệu đi kèm (nguồn gốc, thời gian, tên node vừa chạy...).

---

## 📁 Cấu trúc thư mục Lab 9
- [state.py](file:///d:/AI_LABs/langgraph-learning-labs/labs/09_persistence_threads/state.py): Định nghĩa cấu trúc State của đồ thị.
- [nodes.py](file:///d:/AI_LABs/langgraph-learning-labs/labs/09_persistence_threads/nodes.py): Các node xử lý logic (chuyển câu hỏi thành tin nhắn và gọi LLM).
- [graph.py](file:///d:/AI_LABs/langgraph-learning-labs/labs/09_persistence_threads/graph.py): Xây dựng cấu trúc đồ thị hội thoại (StateGraph).
- `persistence/`:
  - [memory.py](file:///d:/AI_LABs/langgraph-learning-labs/labs/09_persistence_threads/persistence/memory.py): Demo lưu trữ RAM (`InMemorySaver`) và tính cô lập giữa các luồng.
  - [sqlite.py](file:///d:/AI_LABs/langgraph-learning-labs/labs/09_persistence_threads/persistence/sqlite.py): Demo lưu trữ ổ cứng (`SqliteSaver`), nhớ tên người dùng qua nhiều phiên chạy độc lập.
- [inspect_state.py](file:///d:/AI_LABs/langgraph-learning-labs/labs/09_persistence_threads/inspect_state.py): Công cụ truy vấn trạng thái checkpoint hiện tại của thread.
- [inspect_history.py](file:///d:/AI_LABs/langgraph-learning-labs/labs/09_persistence_threads/inspect_history.py): Công cụ truy vấn lịch sử tất cả các checkpoint của thread.
- `tests/`: Bộ kiểm thử tự động xác thực cô lập thread, khôi phục trạng thái và lịch sử.

---

## 🚀 Cách chạy thử nghiệm
1. Chạy kịch bản bộ nhớ RAM:
   ```bash
   python -m labs.09_persistence_threads.persistence.memory
   ```
2. Chạy kịch bản lưu cơ sở dữ liệu SQLite:
   ```bash
   python -m labs.09_persistence_threads.persistence.sqlite
   ```
3. Xem trạng thái hiện tại hoặc lịch sử hội thoại trong file SQLite:
   ```bash
   python -m labs.09_persistence_threads.inspect_state
   python -m labs.09_persistence_threads.inspect_history
   ```
4. Chạy kiểm thử tự động với `pytest`:
   ```bash
   pytest labs/09_persistence_threads/tests/
   ```
