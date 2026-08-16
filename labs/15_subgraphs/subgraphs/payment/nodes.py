from .state import PaymentState
from ...data.data import CUSTOMERS, INVENTORY, ORDERS
import time
from uuid import uuid4


def calculate_node(state: PaymentState):
    products=list(INVENTORY.keys())
    items = state.get("items", [])
    total_amount = 0
    logs=[]
    for item in items:
        if item["name"] in products:
            total_amount += item["quantity"] * item["unit_price"]
        else:
            logs.append(f"❌ Sản phẩm {item['name']} không tồn tại")
    return {
        "total_amount": total_amount,
        "logs": logs,
    }


def process_payment(state: PaymentState):
    logs=[]
    
    order_id=state["order_id"]
    email=[x["customer_email"] for x in ORDERS if x["order_id"]==order_id][0]
    total_amount = state.get("total_amount", 0)
    logs.append(f"Tổng tiền ban đầu: {total_amount:,.0f}VNĐ")

    check_VIP = CUSTOMERS.get(email, {}).get("vip", False)
    logs.append(f"Khách hàng VIP: {check_VIP}")
    
    if check_VIP:
        total_amount *= 0.9
        logs.append(f"Tổng tiền sau khi giảm giá (10% VIP): {total_amount:,.0f}VNĐ")
    
    # 1. Giả lập token hóa thẻ (Tokenization)
    card_token = f"tok_visa_{uuid4().hex[:12]}"

    # 2. Giả lập gọi API cổng thanh toán (Stripe / VNPay / MoMo)
    time.sleep(3)  # Giả lập độ trễ mạng
    transaction_id = f"TXN-{uuid4().hex[:8].upper()}"
    gateway_response = "PAYMENT_SUCCESS_CODE_200"

    return {
        "total_amount": total_amount,
        "card_token": card_token,
        "transaction_id": transaction_id,
        "gateway_response": gateway_response,
        "logs": logs,
    }


def verify_payment(state: PaymentState):
    gateway_response = state.get("gateway_response", "")
    transaction_id = state.get("transaction_id", "")
    logs = []
    if gateway_response == "PAYMENT_SUCCESS_CODE_200":
        logs.append(f"✅ Giao dịch {transaction_id} đã được xác thực thành công")
        return {"payment_success": True, "logs": logs}
    else:
        logs.append(f"❌ Giao dịch {transaction_id} thất bại")
        return {"payment_success": False, "logs": logs}


if __name__ == "__main__":
    test_state: PaymentState = {
        "order_id": "ORD-001",
        "customer_name": "Nguyễn Văn An",
        "customer_email": "an.nguyen@email.com",
        "items": [
            {"name": "Laptop Dell XPS 15", "quantity": 1, "unit_price": 35000000},
            {"name": "Chuột Logitech MX Master", "quantity": 2, "unit_price": 2500000},
        ],
        "card_token": "",
        "transaction_id": "",
        "gateway_response": "",
        "total_amount": 0,
        "payment_success": False,
        "logs": [],
    }

    # 1. Test calculate
    c_res = calculate_node(test_state)
    test_state.update(c_res)
    print(f"\n--- 1. calculate_node: {test_state['total_amount']:,.0f} VNĐ ---")

    # 2. Test process
    p_res = process_payment(test_state)
    test_state.update(p_res)
    print(f"--- 2. process_payment: card_token={test_state['card_token']}, txn={test_state['transaction_id']} ---")

    # 3. Test verify
    v_res = verify_payment(test_state)
    test_state.update(v_res)
    print(f"--- 3. verify_payment: success={test_state['payment_success']} ---")

    print("\n--- ALL LOGS ---")
    for log in c_res["logs"] + p_res["logs"] + v_res["logs"]:
        print(f"  {log}")