import json
import re

from state import TravelState
from shared.models import GroqLLMModel

def json_extract(response):
    text = response.content
    try:
        # Tiền xử lý: Thay thế các phép tính cộng trong chuỗi (ví dụ: 2500000 + 600000) thành kết quả số nguyên
        text = re.sub(
            r'\d+(?:\s*\+\s*\d+)+',
            lambda m: str(sum(int(x) for x in m.group(0).replace(' ', '').split('+'))),
            text
        )
    except Exception:
        pass

    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                print("JSON is invalid")
                print(match.group(0))
                pass
        return {}

def vehicle_booking(state: TravelState):
    query = state['input']
    model = GroqLLMModel()

    prompt = f"""Bạn là trợ lý du lịch. Nhiệm vụ của bạn là CHỈ trích xuất thông tin liên quan đến PHƯƠNG TIỆN DI CHUYỂN (vé máy bay, vé tàu, vé xe, phương tiện đi lại) từ yêu cầu của người dùng: "{query}".
    Hãy bỏ qua hoàn toàn các thông tin về đặt phòng khách sạn hoặc hoạt động ăn chơi khác.

    Trả về định dạng JSON duy nhất sau:
    {{
        "destination": "tên thành phố/điểm đến (ví dụ: Nha Trang, Đà Lạt)",
        "total_cost": số_tiền_vé_phương_tiện (CHỈ ĐƯỢC trả về một số nguyên duy nhất, ví dụ: 2500000. TUYỆT ĐỐI không viết phép tính cộng trừ, không để trong dấu nháy kép),
        "itinerary": ["Nội dung di chuyển (ví dụ: Bay đến Nha Trang)"],
        "checklist": {{"Vé máy bay/tàu/xe": true, "Căn cước công dân": true}}
    }}
    Chú ý: Chỉ trả về chuỗi JSON thô, không viết thêm lời dẫn.
    """
    response = model.invoke(prompt)
    extracted_data= json_extract(response)
    print("- vehicle_booking:")
    print(json.dumps(extracted_data, ensure_ascii=False, indent=2))
    return extracted_data

def hotel_booking(state: TravelState):
    query = state['input']
    model = GroqLLMModel()

    prompt = f"""Bạn là trợ lý du lịch. Nhiệm vụ của bạn là CHỈ trích xuất thông tin liên quan đến ĐẶT PHÒNG KHÁCH SẠN từ yêu cầu của người dùng: "{query}".
    Hãy bỏ qua hoàn toàn các thông tin về phương tiện di chuyển hoặc hoạt động ăn chơi khác.

    Trả về định dạng JSON duy nhất sau:
    {{
        "destination": "tên thành phố/điểm đến (ví dụ: Nha Trang, Đà Lạt)",
        "total_cost": số_tiền_đặt_phòng (CHỈ ĐƯỢC trả về một số nguyên duy nhất đại diện cho tiền khách sạn, ví dụ: 3000000. TUYỆT ĐỐI không viết phép tính cộng trừ, không cộng dồn các chi phí khác, không để trong dấu nháy kép),
        "itinerary": ["Nội dung đặt phòng khách sạn (ví dụ: Đặt phòng khách sạn tại Nha Trang)"],
        "checklist": {{"Đặt phòng khách sạn": true, "Chứng minh nhân dân": true}}
    }}
    Chú ý: Chỉ trả về chuỗi JSON thô, không viết thêm lời dẫn.
    """
    response = model.invoke(prompt)
    extracted_data= json_extract(response)
    print("- hotel_booking:")
    print(json.dumps(extracted_data, ensure_ascii=False, indent=2))
    return extracted_data

def itinerary_planning(state: TravelState):
    query = state['input']
    model = GroqLLMModel()

    prompt = f"""Bạn là trợ lý du lịch. Nhiệm vụ của bạn là CHỈ trích xuất thông tin liên quan đến HOẠT ĐỘNG VUI CHƠI, GIẢI TRÍ, THAM QUAN, ĂN UỐNG từ yêu cầu của người dùng: "{query}".
    Hãy bỏ qua hoàn toàn các thông tin về phương tiện di chuyển hoặc phòng khách sạn.

    Trả về định dạng JSON duy nhất sau:
    {{
        "destination": "tên thành phố/điểm đến (ví dụ: Nha Trang, Đà Lạt)",
        "total_cost": chi_phí_vui_chơi (CHỈ ĐƯỢC trả về một số nguyên duy nhất, ví dụ: 600000. TUYỆT ĐỐI không viết phép tính cộng trừ, không để trong dấu nháy kép),
        "itinerary": ["Nội dung hoạt động (ví dụ: Tham quan Vinpearl Land Nha Trang)"],
        "checklist": {{"Giày thể thao": true, "Kem chống nắng": true}}
    }}
    Chú ý: Chỉ trả về chuỗi JSON thô, không viết thêm lời dẫn.
    """
    response = model.invoke(prompt)
    extracted_data = json_extract(response)
    print("- itinerary_planning:")
    print(json.dumps(extracted_data, ensure_ascii=False, indent=2))
    return extracted_data