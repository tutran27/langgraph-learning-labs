import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import graph

if __name__ == "__main__":
    initial_state = {
        "input": "Tôi muốn đi du lịch Nha Trang, đặt vé máy bay khứ hồi hết 2500000đ, đặt phòng khách sạn Sheraton hết 3000000đ, và mua vé tắm bùn Hòn Tằm mất 600000đ."
    }

    print("=== Execution ===")
    final_state = graph.invoke(initial_state)

    print("\n=== Final State ===")
    print(f"Destination: {final_state.get('destination')}")
    print(f"Total Cost: {final_state.get('total_cost')}đ")
    
    print("Itinerary:")
    for step in final_state.get('itinerary', []):
        print(f"  - {step}")
        
    print("Checklist:")
    checklist = final_state.get('checklist', {})
    for item, status in checklist.items():
        print(f"  - {item}: {status}")
