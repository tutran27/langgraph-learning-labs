# 🚀 LangGraph Learning Labs

Chào mừng bạn đến với **LangGraph Learning Labs**! Kho lưu trữ này được thiết kế để cung cấp các bài thực hành từ cơ bản đến nâng cao về xây dựng AI Agent sử dụng thư viện **LangGraph** của LangChain.

---

## 📂 Tổ chức dự án

Dự án được cấu trúc theo dạng mô-đun khoa học, tách biệt giữa thư viện chia sẻ chung (`shared/`), các bài lab học tập (`labs/`), ứng dụng thực tế (`projects/`), và hệ thống kiểm thử (`tests/`).

```text
langgraph-labs/
├── 📁 shared/                  # Cấu hình, model giả lập và helper dùng chung
├── 📁 labs/                    # 19 bài Lab từ cơ bản đến nâng cao
│   ├── 01_first_state_graph/   # Khởi tạo đồ thị trạng thái đơn giản nhất
│   ├── 02_state_and_reducers/  # Xử lý cập nhật State & Reducers chuyên sâu
│   ├── 03_edges_and_routing/   # Định tuyến điều kiện (Conditional Routing)
│   ├── 04_cycles_and_limits/   # Vòng lặp tuần hoàn & Cơ chế ngắt giới hạn
│   ├── 05_parallel_execution/  # Chạy song song nhiều node & Fan-out / Fan-in
│   ├── 06_send_map_reduce/     # Bản đồ phân tán động sử dụng lệnh Send
│   ├── 07_command_control/     # Điều phối luồng linh hoạt với Command API
│   ├── 08_functional_api/      # Tiếp cận Functional API tiên tiến (v1.2+)
│   ├── 09_persistence_threads/ # Lưu trữ trạng thái (Persistence & Checkpointers)
│   ├── 10_interrupt_approval/  # Tương tác con người (HITL - Human-in-the-loop)
│   ├── 11_time_travel/         # Khả năng "du hành thời gian" & Fork nhánh State
│   ├── 12_short_long_memory/   # Quản lý bộ nhớ ngắn hạn & dài hạn (Store)
│   ├── 13_streaming_events/    # Truyền phát sự kiện thời gian thực (Streaming v2/v3)
│   ├── 14_fault_tolerance/     # Xử lý ngoại lệ, Retry và Timeout cho Node
│   ├── 15_subgraphs/           # Tổ chức phân cấp nhiều đồ thị con (SubGraph)
│   ├── 16_tool_calling_agent/  # Tạo tác vụ gọi công cụ ngoài (Tool-calling)
│   ├── 17_agentic_rag/         # Xây dựng luồng RAG thông minh (Corrective RAG)
│   ├── 18_multi_agent/         # Thiết kế hệ thống đa tác nhân (Multi-agent System)
│   └── 19_production_graph/    # Đóng gói đồ thị lên sản phẩm (Production Ready)
├── 📁 projects/                # Các dự án mẫu ứng dụng thực tiễn
├── 📁 tests/                   # Kịch bản kiểm thử tự động (PyTest)
├── 📄 requirements.txt         # Quản lý thư viện phụ thuộc
└── 📄 pyproject.toml           # Cấu hình dự án Python chuẩn
```

---

## 🛠️ Yêu cầu cài đặt

### 1. Chuẩn bị môi trường
Khuyến nghị sử dụng Python phiên bản **3.10 trở lên**. Bạn nên tạo môi trường ảo trước khi cài đặt:

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo (Windows)
.venv\Scripts\activate

# Kích hoạt môi trường ảo (macOS/Linux)
source .venv/bin/activate
```

### 2. Cài đặt các thư viện phụ thuộc
Cài đặt toàn bộ công cụ cần thiết từ tệp `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🧪 Chạy thử nghiệm kiểm thử (Testing)

Mỗi bài Lab đều đi kèm với các kịch bản kiểm thử tự động bằng **PyTest**. Bạn có thể kiểm tra tính chính xác của mã nguồn bằng cách chạy:

```bash
# Chạy tất cả các test trong dự án
pytest

# Chạy test của một bài lab cụ thể (ví dụ Lab 01)
pytest labs/01_first_state_graph/
```

---

## 💡 Các tính năng nổi bật của LangGraph (v1.2+)

- **State Management & Reducers**: Quản lý trạng thái Agent linh hoạt thông qua các kiểu Schema và cơ chế tích hợp dữ liệu (reducers).
- **Persistence & Time Travel**: Tự động lưu checkpoint, cho phép khôi phục lịch sử hoặc chạy nhánh phụ (fork) bất kỳ lúc nào.
- **Human-in-the-Loop**: Dễ dàng tích hợp bước phê duyệt hoặc điều chỉnh từ con người trước khi thực hiện tác vụ quan trọng.
- **Multi-agent Orchestration**: Cho phép phân rã bài toán phức tạp thành nhiều đồ thị con hoạt động độc lập hoặc dưới sự chỉ đạo của Supervisor.

---
⭐ *Hãy tận hưởng hành trình học tập lập trình AI Agent cùng LangGraph!*
