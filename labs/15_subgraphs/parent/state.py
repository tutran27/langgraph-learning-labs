"""
Parent State — E-Commerce Order Pipeline

Chứa các trường SHARED mà tất cả subgraphs đều có thể nhìn thấy.
Mỗi subgraph chỉ nhận một phần của ParentState thông qua adapter,
và trả kết quả về qua adapter (không truy cập trực tiếp).

Flow: receive_order → validation → payment → fulfillment → compile_result
"""

import operator
from typing import Annotated, List
from typing_extensions import TypedDict


class OrderItem(TypedDict):
    name: str
    quantity: int
    unit_price: float


class ParentState(TypedDict):
    # --- Thông tin đơn hàng ---
    order_id: str
    customer_name: str
    customer_email: str
    customer_address: str
    items: List[OrderItem]

    # --- Kết quả từ subgraphs ---
    validation_passed: bool          # ← từ validation subgraph
    total_amount: float              # ← từ payment subgraph
    payment_success: bool            # ← từ payment subgraph
    tracking_id: str                 # ← từ fulfillment subgraph

    # --- Trạng thái chung ---
    status: str                      # "received" → "validated" → "paid" → "shipped" → "completed"
    logs: Annotated[List[str], operator.add]
