# Lab 02 · State and Reducers

> 🧬 Cơ chế quản lý trạng thái và gộp dữ liệu (Reducers): từ ghi đè mặc định, cộng dồn list đến custom reducer.

## 🎯 Mục tiêu

- Sử dụng `Annotated` kết hợp hàm Reducer trên State.
- Phân biệt Override mặc định vs Accumulate (`operator.add`).
- Tự viết Custom Reducer gộp dictionary không mất dữ liệu.
- Hiểu cách dữ liệu từ nhiều node hội tụ vào State tổng.

## 📂 Cấu trúc & Ý tưởng (Travel Planner)

- **`state.py`**: `TravelState` với Reducer tương ứng cho từng loại dữ liệu.
- **`reducers.py`**: Custom reducer `merge_checklist` gộp dict.
- **`nodes.py`**: Trích xuất từng phần (phương tiện, khách sạn, vui chơi).
- **`graph.py`**: Đăng ký nodes và liên kết thành đồ thị.
- **`run.py`**: Thực thi đồ thị và hiển thị kết quả gộp.
- **`experiments.py`**: Thử nghiệm nhanh hành vi Reducers.

## ⚙️ Hướng dẫn khởi chạy

```bash
python -m labs.02_state_and_reducers.run
```

```bash
python -m pytest labs/02_state_and_reducers/tests -v
```
