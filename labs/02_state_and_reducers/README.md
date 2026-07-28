# Lab 02 · State and Reducers

> 🧬 Tìm hiểu cơ chế quản lý trạng thái và các phương thức gộp dữ liệu (Reducers) từ cơ bản, cộng dồn list đến custom reducer tự viết.

## 🎯 Mục tiêu

- Định nghĩa State nâng cao sử dụng `typing.Annotated` kết hợp các hàm Reducer.
- So sánh sự khác biệt giữa ghi đè mặc định (Override) và cộng dồn (Accumulate) bằng `operator.add`.
- Tự viết một hàm Custom Reducer để gộp dữ liệu dạng từ điển (Dictionary Merger) không làm mất mát thông tin.
- Hiểu cách dữ liệu từ nhiều node độc lập tự động hội tụ và đồng bộ vào State tổng.

## 📂 Nội dung hiện có

| File | Mô tả | Cách chạy |
| --- | --- | --- |
| `state.py` | Khai báo `TravelState` sử dụng các Reducer tương ứng cho từng loại dữ liệu | - |
| `reducers.py` | Cài đặt hàm custom reducer `merge_checklist` dùng để gộp dict | - |
| `nodes.py` | Trích xuất thông tin từng phần (phương tiện, khách sạn, vui chơi) từ một câu đầu vào | - |
| `graph.py` | Đăng ký các node trích xuất và liên kết thành đồ thị chạy tuần tự | - |
| `run.py` | Script nạp câu lệnh mẫu thực thi đồ thị và hiển thị kết quả gộp của các Reducers | `python -m labs.02_state_and_reducers.run` |
| `experiments.py` | File nháp thử nghiệm nhanh hành vi của Reducers | `python -m labs.02_state_and_reducers.experiments` |
