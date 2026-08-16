import json 
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def read_json(filename):
    if not filename.endswith(".json"):
        filename = f"{filename}.json"
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

DATA = {}
if os.path.exists(DATA_DIR):
    for file in os.listdir(DATA_DIR):
        if file.endswith(".json"):
            key = file[:-5]
            DATA[key] = read_json(file)

INVENTORY = DATA.get("inventory", {}).get("inventory", {})
CUSTOMERS = DATA.get("customers", {}).get("customers", {})
WAREHOUSES = DATA.get("warehouses", {}).get("warehouses", {})
ORDERS = DATA.get("orders", {}).get("orders", [])

if __name__ == "__main__":
    print(f"================= DATA (Loaded from {DATA_DIR}) =================")
    for k, v in DATA.items():
        print(f"---------- {k.upper()} ----------")
        print(json.dumps(v, indent=2, ensure_ascii=False))
    print(f"=============================================")
