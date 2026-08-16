import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import graph

if __name__ == "__main__":
    cases = [
        "CRITICAL: CPU temperature is 95C",
        "INFO: normal flow logs",
        200,
        503,
        None,
        {"status": "error"}
    ]
    
    for case in cases:
        print(f"\n==========================================")
        print(f"Testing input_data: {case} ({type(case).__name__})")
        initial_state = {"input_data": case}
        
        final_state = graph.invoke(initial_state)
        
        print(f"Result: {final_state.get('processed_result')}")
        print(f"Routing Reason: {final_state.get('routing_reason')}")
