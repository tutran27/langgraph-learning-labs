"""
Payment Subgraph State

Private state cho việc xử lý thanh toán.
Parent KHÔNG nhìn thấy: card_token, transaction_id, gateway_response.
Parent CHỈ nhận lại: total_amount, payment_success (qua adapter).

Nodes: calculate_total → process_payment → verify_payment
"""

import operator
from typing import Annotated, List
from typing_extensions import TypedDict

from ...parent.state import OrderItem


class PaymentState(TypedDict):
    # --- Shared (nhận từ parent qua adapter) ---
    order_id: str
    items: List[OrderItem]

    # --- Private (chỉ tồn tại trong subgraph) ---
    card_token: str                  # Token thẻ thanh toán (nhạy cảm, không lộ ra parent)
    transaction_id: str              # Mã giao dịch từ cổng thanh toán
    gateway_response: str            # Phản hồi raw từ payment gateway

    # --- Output (trả về parent qua adapter) ---
    total_amount: float              # Tổng tiền đã tính
    payment_success: bool            # Thanh toán thành công hay không
    logs: Annotated[List[str], operator.add]
