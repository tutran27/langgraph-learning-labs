"""
Validation Subgraph State

Private state cho việc kiểm tra đơn hàng.
Parent KHÔNG nhìn thấy: stock_levels, address_valid, customer_verified.
Parent CHỈ nhận lại: validation_passed (qua adapter).

Nodes: check_inventory → validate_address → validate_customer
"""

import operator
from typing import Annotated, Dict, List
from typing_extensions import TypedDict

from ...parent.state import OrderItem


class ValidationState(TypedDict):
    # --- Shared (nhận từ parent qua adapter) ---
    order_id: str
    items: List[OrderItem]
    customer_name: str
    customer_email: str
    customer_address: str

    # --- Private (chỉ tồn tại trong subgraph) ---
    stock_levels: Dict[str, int]     # {item_name: số lượng tồn kho}
    address_valid: bool              # Kết quả kiểm tra địa chỉ
    customer_verified: bool          # Kết quả xác minh khách hàng

    # --- Output (trả về parent qua adapter) ---
    validation_passed: bool          # Tổng kết: True nếu tất cả đều pass
    logs: Annotated[List[str], operator.add]
