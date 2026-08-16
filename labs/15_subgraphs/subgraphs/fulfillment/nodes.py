from uuid import uuid4
from ...data.data import INVENTORY, WAREHOUSES
from .state import FulfillmentState

PREFERRED_CARRIERS = ["GHN", "GHTK", "Viettel Post", "VNPost", "J&T Express"]


def assign_warehouse(state: FulfillmentState) -> dict:
    order_id = state.get("order_id", "")
    items = state.get("items", [])
    logs = []
    warehouse_id = []
    list_products = list(INVENTORY.keys())

    for item in items:
        name = item.get("name", "")
        if name not in list_products:
            logs.append(f"❌ Order {order_id}: Sản phẩm '{name}' không có trong kho")
            continue

        wh = INVENTORY[name].get("warehouse")
        if wh and wh not in warehouse_id:
            warehouse_id.append(wh)

    if not warehouse_id:
        logs.append("❌ Không tìm thấy kho nào còn hàng cho đơn này")
    else:
        logs.append(f"📦 Đơn hàng {order_id} được phân phối tới kho: {', '.join(warehouse_id)}")

    return {
        "warehouse_id": warehouse_id,
        "logs": logs,
    }


def create_shipment(state: FulfillmentState) -> dict:
    warehouse_id = state.get("warehouse_id", [])
    order_id = state.get("order_id", "")
    address = state.get("customer_address", "")
    logs = []
    carriers = []

    if not warehouse_id:
        return {
            "carriers": [],
            "tracking_id": "N/A",
            "estimated_delivery": "N/A",
            "logs": ["❌ Không có kho xuất hàng để tạo vận đơn"],
        }

    # Chọn carrier ưu tiên cho từng kho
    for wh_id in warehouse_id:
        wh_carriers = WAREHOUSES.get(wh_id, {}).get("carriers", [])
        chosen_carrier = None
        for c in PREFERRED_CARRIERS:
            if c in wh_carriers:
                chosen_carrier = c
                break
        if not chosen_carrier and wh_carriers:
            chosen_carrier = wh_carriers[0]

        if chosen_carrier and chosen_carrier not in carriers:
            carriers.append(chosen_carrier)

        logs.append(f"🚚 Kho {wh_id} xuất hàng qua đơn vị: {chosen_carrier or 'Mặc định'}")

    # Tính thời gian giao hàng (an toàn khi có kho)
    is_same_city = all(WAREHOUSES[wh]["city"] in address for wh in warehouse_id) if warehouse_id else False
    estimated_delivery = "1-2 ngày" if is_same_city else "2-4 ngày"

    # Tạo mã vận đơn tracking
    main_carrier = carriers[0] if carriers else "VNPost"
    tracking_id = f"TRACK-{main_carrier}-{uuid4().hex[:8].upper()}"

    logs.append(f"🏷️ Đã tạo mã vận đơn: {tracking_id} (Dự kiến giao: {estimated_delivery})")

    return {
        "carriers": carriers,
        "tracking_id": tracking_id,
        "estimated_delivery": estimated_delivery,
        "logs": logs,
    }


def send_notification(state: FulfillmentState) -> dict:
    email = state.get("customer_email", "")
    tracking_id = state.get("tracking_id", "")
    est = state.get("estimated_delivery", "")
    carriers_str = ", ".join(state.get("carriers", []))

    logs = [
        f"📧 Đã gửi email xác nhận giao hàng tới {email}",
        f"   Đơn vị vận chuyển: {carriers_str} | Mã vận đơn: {tracking_id} | Dự kiến: {est}",
    ]
    return {
        "notification_sent": True,
        "logs": logs,
    }


if __name__ == "__main__":
    test_state: FulfillmentState = {
        "order_id": "ORD-001",
        "customer_name": "Nguyễn Văn An",
        "customer_email": "an.nguyen@email.com",
        "customer_address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
        "items": [
            {"name": "Laptop Dell XPS 15", "quantity": 1, "unit_price": 35000000},
            {"name": "Chuột Logitech MX Master", "quantity": 2, "unit_price": 2500000},
        ],
        "warehouse_id": [],
        "carriers": [],
        "estimated_delivery": "",
        "notification_sent": False,
        "tracking_id": "",
        "logs": [],
    }

    # 1. Assign warehouse
    res1 = assign_warehouse(test_state)
    test_state.update(res1)

    # 2. Create shipment
    res2 = create_shipment(test_state)
    test_state.update(res2)

    # 3. Send notification
    res3 = send_notification(test_state)
    test_state.update(res3)

    print(f"\n--- KẾT QUẢ TEST FULFILLMENT (ORD-001) ---")
    print(f"Kho: {test_state['warehouse_id']}")
    print(f"Carriers: {test_state['carriers']}")
    print(f"Tracking ID: {test_state['tracking_id']}")
    print(f"Dự kiến: {test_state['estimated_delivery']}")
    print(f"Đã gửi mail: {test_state['notification_sent']}")
    print("\n--- ALL LOGS ---")
    for log in res1["logs"] + res2["logs"] + res3["logs"]:
        print(f"  {log}")
    
        