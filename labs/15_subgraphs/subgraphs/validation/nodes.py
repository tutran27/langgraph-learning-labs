from ..validation.state import ValidationState
from ...data.data import INVENTORY, CUSTOMERS


def check_inventory(state: ValidationState) -> dict:
    products_name=[p for p in INVENTORY.keys()]
    stock_levels = {}
    logs = []
    all_ok = bool(state.get("items"))
    print(f"Initialize All OK: {all_ok}")

    for item in state.get("items", []):
        name = item.get("name", "")
        if name not in products_name:
            all_ok=False
            logs.append(f"❌ Sản phẩm {name} không tồn tại")
            
        qty = item.get("quantity", 0)
        stock = INVENTORY.get(name, {}).get("stock", 0)
        stock_levels[name] = stock

        if stock < qty or qty <= 0:
            all_ok = False
            logs.append(f"❌ {name}: thiếu hàng cho {name} ( đặt {qty}, kho còn {stock})")
        else:
            logs.append(f"✅ {name}: đủ hàng cho {name} ( đặt {qty}, kho còn {stock})")

    return {
        "stock_levels": stock_levels,
        "validation_passed": all_ok,
        "logs": logs or ["❌ Đơn hàng rỗng"],
    }


def validate_address(state: ValidationState) -> dict:
    addr = state.get("customer_address", "").strip()
    valid = len(addr) > 2
    passed = state.get("validation_passed", True) and valid
    log = f"✅ Địa chỉ hợp lệ: {addr}" if valid else "❌ Địa chỉ không hợp lệ"
    return {"address_valid": valid, 
            "validation_passed": passed, 
            "logs": [log]}


def validate_customer(state: ValidationState) -> dict:
    name=state.get("customer_name", "").strip()
    email = state.get("customer_email", "").strip()
    email_verified = CUSTOMERS.get(email, {}).get("verified", False)

    passed = state.get("validation_passed", True) and email_verified
    log = f"✅ Khách hàng {name} đã xác minh: {email}" if email_verified else f"❌ Khách hàng {name} chưa xác minh: {email}"
    return {"customer_verified": email_verified, 
            "validation_passed": passed, 
            "logs": [log]}

if __name__ == "__main__":
    state = {
        "order_id": "ORD-001",
        "customer_name": "John Doe",
        "customer_email": "[EMAIL_ADDRESS]",
        "customer_address": "123 Main St",
        "items": [
            {"name": "Laptop", "quantity": 1},
            {"name": "Chuột Logitech MX Master", "quantity": 1},
        ],
    }

    result = check_inventory(state)
    print(f"\n--- Test check_inventory(ORD-001) ---")
    for log in result["logs"]:
        print(f"  {log}")

    state["validation_passed"] = result["validation_passed"]
    result = validate_address(state)
    print(f"\n--- Test validate_address(ORD-001) ---")
    print(f"Passed: {result['address_valid']}")
    for log in result["logs"]:
        print(f"  {log}")

    state["validation_passed"] = result["validation_passed"]
    result = validate_customer(state)
    print(f"\n--- Test validate_customer(ORD-001) ---")
    print(f"Passed: {result['customer_verified']}")
    for log in result["logs"]:
        print(f"  {log}")

    state["validation_passed"] = result["validation_passed"]
    print(f"\n--- Test get_information(ORD-001) ---")
    print(f"Passed: {result['validation_passed']}")
    for log in result["logs"]:
        print(f"  {log}")
