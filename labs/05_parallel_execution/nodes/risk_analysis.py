import asyncio
from state import AnalysisState

async def risk_analysis_node(state: AnalysisState):
    company = state.get("company", "N/A")
    print(f"  --> [Risk Analysis] Analyzing {company}...")
    await asyncio.sleep(1.0)
    
    report = {
        "type": "risk",
        "title": "Risk Assessment",
        "details": f"Rủi ro chuỗi cung ứng ở mức trung bình, rủi ro pháp lý thấp đối với {company}."
    }
    return {"reports": [report]}
