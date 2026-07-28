# LangGraph Learning Labs

> 🚀 Bộ bài thực hành và tài liệu nghiên cứu tự học LangGraph theo lộ trình tăng dần, từ đồ thị trạng thái cơ bản đến persistence, human-in-the-loop, streaming, RAG và multi-agent workflows.

## 🎯 Mục tiêu tìm hiểu

Repository này được tổ chức để phục vụ việc tự nghiên cứu:
- Tìm hiểu các khái niệm cốt lõi của LangGraph qua từng lab nhỏ độc lập, dễ chạy và dễ debug.
- Thực hành xây dựng các mẫu thiết kế Agent (Agentic Patterns) khác nhau.
- Làm quen với cơ chế quản lý State, Reducers, Checkpointers, Memory và Streaming trong LangGraph.
- Tích hợp kiểm thử tự động (`pytest` kết hợp mock LLM) để tối ưu hóa quy trình phát triển.

## 📂 Cấu trúc dự án

Dự án được cấu trúc dạng mô-đun để dễ dàng cô lập và quản lý các bài thực hành:

```text
langgraph-labs/
├── 📁 shared/                  # Cấu hình model và helper dùng chung (Groq, Config)
├── 📁 labs/                    # 19 bài Lab nghiên cứu từ cơ bản đến nâng cao
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
├── 📄 requirements.txt         # Thư viện phụ thuộc
└── 📄 pyproject.toml           # Cấu hình dự án Python chuẩn
```

## ⚙️ Cài đặt & Sử dụng

### 1. Chuẩn bị môi trường
Khuyến nghị sử dụng Python phiên bản **3.10 trở lên** với môi trường ảo `conda` hoặc `venv`:

```bash
# Tạo và kích hoạt môi trường ảo
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Cài đặt thư viện phụ thuộc
pip install -r requirements.txt
```

### 2. Thiết lập biến môi trường
Tạo file `.env` ở thư mục gốc của dự án và cấu hình các khóa API cần thiết:
```env
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.1-8b-instant
LANGCHAIN_TRACING_V2=false
```

---

## 🧪 Quy trình kiểm thử (Testing)

Hệ thống sử dụng **pytest** để tự động kiểm thử các node và đồ thị mà không cần gọi API thật (thông qua cơ chế mock):

```bash
# Chạy toàn bộ các test trong dự án
pytest

# Chạy riêng bộ test của Lab 01
pytest labs/01_first_state_graph/
```

---

## 💡 Các nội dung cốt lõi của LangGraph cần nắm vững

Trong suốt lộ trình thực hành, tập trung làm rõ các đặc trưng kỹ thuật sau của LangGraph:
- **State & Reducers**: Cách dữ liệu tích lũy và cập nhật đè qua các node.
- **Persistence (Checkpointers)**: Cho phép lưu trạng thái của luồng chạy để khôi phục hoặc du hành thời gian (Time Travel).
- **Human-in-the-loop (HITL)**: Cơ chế ngắt tạm thời (Interrupt) để chờ phê duyệt hoặc bổ sung dữ liệu từ con người.
- **Multi-agent Architectures**: Các mô hình kết nối nhiều tác nhân độc lập (Multi-agent) sử dụng Subgraphs hoặc Router.
