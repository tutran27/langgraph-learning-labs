"""
Fulfillment Subgraph State

Private state cho việc giao hàng.
Parent KHÔNG nhìn thấy: warehouse_id, carrier, estimated_delivery, notification_sent.
Parent CHỈ nhận lại: tracking_id (qua adapter).

Nodes: assign_warehouse → create_shipment → send_notification
"""

from typing import Annotated, List
from typing_extensions import TypedDict
import operator

from ...parent.state import OrderItem

class FulfillmentState(TypedDict):
    # --- Shared (nhận từ parent qua adapter) ---
    order_id: str
    customer_name: str
    customer_email: str
    customer_address: str
    items: List[OrderItem]

    # --- Private (chỉ tồn tại trong subgraph) ---
    warehouse_id: List[str]          # Danh sách mã kho được phân phối
    carriers: List[str]              # Đơn vị vận chuyển (GHN, GHTK, VNPost...)
    estimated_delivery: str          # Ngày giao hàng dự kiến
    notification_sent: bool          # Đã gửi thông báo cho khách chưa

    # --- Output (trả về parent qua adapter) ---
    tracking_id: str                 # Mã vận đơn
    logs: Annotated[List[str], operator.add]
