# Lab 10: Human-in-the-loop (HITL) - Cơ chế Interrupt và Approval trong LangGraph

Lab này hướng dẫn cách xây dựng một luồng hội thoại kết hợp phê duyệt hành động có sự can thiệp của con người (**Human-in-the-loop**). Chúng ta sẽ tìm hiểu cách sử dụng hàm ngắt động **`interrupt()`** (một tính năng mạnh mẽ từ LangGraph v0.2.x / v1.x+) để dừng đồ thị ngay tại thời điểm thực thi của Node và tiếp tục chạy thông qua lệnh **`Command(resume=...)`**.

---

## 🎯 Mục tiêu bài học
* Hiểu mô hình **Human-in-the-loop (HITL)** và tầm quan trọng của nó đối với các hành động nhạy cảm (chuyển tiền, gửi email, chạy code,...).
* Thành thạo cách sử dụng hàm ngắt động **`interrupt()`** trong Node để dừng đồ thị và trả thông tin ra bên ngoài Client.
* Biết cách sử dụng **`Command(resume=...)`** từ phía Client để truyền quyết định phê duyệt và đánh thức đồ thị chạy tiếp.
* Cách thiết kế đồ thị rẽ nhánh có điều kiện dựa trên trạng thái phê duyệt động.

---

## 🔑 Các khái niệm cốt lõi

*   **Human-in-the-loop (HITL)**: Mẫu thiết kế trong phát triển AI Agent, nơi con người giám sát, phê duyệt hoặc cung cấp thông tin phản hồi cho Agent trước khi thực hiện các tác vụ có tính rủi ro hoặc bảo mật cao.
*   **Dynamic Interrupt (`interrupt()`)**: Hàm ngắt động được khai báo trực tiếp bên trong logic xử lý của Node. Khi đồ thị chạy đến dòng code này, nó sẽ tự động dừng lại, lưu checkpoint vào bộ nhớ, và trả về dữ liệu ngắt cho Client.
*   **Command(resume=value)**: Lớp điều khiển được Client sử dụng khi tiếp tục phiên chạy (`stream` / `invoke`). Dữ liệu trong `resume` sẽ được chuyển thẳng vào giá trị trả về của hàm `interrupt()` bên trong Node đang bị tạm dừng.

---

## 📁 Cấu trúc thư mục Lab 10
*   [state.py](file:///d:/LABs/langgraph_learning_labs/labs/10_interrupt_approval/state.py): Định nghĩa cấu trúc `ApprovalState` dùng để lưu trữ hội thoại, hành động trích xuất và trạng thái phê duyệt.
*   `nodes/`:
    *   [prepare_action.py](file:///d:/LABs/langgraph_learning_labs/labs/10_interrupt_approval/nodes/prepare_action.py): Sử dụng LLM phân tích câu chat của người dùng để quyết định câu hỏi thường hay là hành động nhạy cảm cần phê duyệt.
    *   [request_approval.py](file:///d:/LABs/langgraph_learning_labs/labs/10_interrupt_approval/nodes/request_approval.py): Chứa lệnh ngắt `interrupt()` để tạm dừng đồ thị và chờ quyết định từ CLI.
    *   [execute_action.py](file:///d:/LABs/langgraph_learning_labs/labs/10_interrupt_approval/nodes/execute_action.py): Thực thi giả lập và in kết quả hành động thành công nếu được duyệt.
    *   [reject_action.py](file:///d:/LABs/langgraph_learning_labs/labs/10_interrupt_approval/nodes/reject_action.py): Trả về thông báo từ chối kèm lý do phản hồi nếu không được duyệt.
*   [routers.py](file:///d:/LABs/langgraph_learning_labs/labs/10_interrupt_approval/routers.py): Định tuyến điều hướng luồng đi tiếp dựa trên kết quả phê duyệt trong State.
*   [graph.py](file:///d:/LABs/langgraph_learning_labs/labs/10_interrupt_approval/graph.py): Xây dựng cấu trúc đồ thị hội thoại (StateGraph) kết hợp Checkpointer lưu trữ trạng thái.
*   [cli_approval.py](file:///d:/LABs/langgraph_learning_labs/labs/10_interrupt_approval/cli_approval.py): Chương trình giao diện dòng lệnh (CLI) tương tác trực tiếp với người dùng và thực hiện cơ chế duyệt thông qua Command.

---

## 🚀 Cách chạy thử nghiệm

1.  Mở terminal tại thư mục gốc dự án (`langgraph_learning_labs`).
2.  Chạy chương trình tương tác CLI:
    ```bash
    python -m labs.10_interrupt_approval.cli_approval
    ```
3.  **Kịch bản kiểm thử gợi ý:**
    *   *Kịch bản chat thường:* Nhập `"hi"`, `"hello"` hoặc hỏi đáp thông thường. Đồ thị sẽ trả lời tự nhiên qua LLM mà không kích hoạt ngắt phê duyệt.
    *   *Kịch bản duyệt thành công:* Nhập `"tôi muốn chuyển 5 triệu cho Tú"`. Hệ thống sẽ cảnh báo yêu cầu phê duyệt $\rightarrow$ Chọn `y` $\rightarrow$ Đồ thị tiếp tục chạy và in ra thông báo thực thi thành công.
    *   *Kịch bản từ chối:* Nhập `"tôi muốn gửi email cho CEO"`. Chọn `n` $\rightarrow$ Nhập lý do từ chối $\rightarrow$ Đồ thị tiếp tục và thông báo từ chối kèm lý do.
