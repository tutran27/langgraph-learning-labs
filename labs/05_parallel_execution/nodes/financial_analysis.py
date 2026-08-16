import asyncio
from state import AnalysisState

async def financial_analysis_node(state: AnalysisState):
    company = state.get("company", "N/A")
    print(f"  --> [Financial Analysis] Analyzing {company}...")
    await asyncio.sleep(1.0)
    
    report = {
        "type": "financial",
        "title": "Financial Report",
        "details": f"Doanh thu của {company} tăng trưởng 15% so với cùng kỳ, dòng tiền hoạt động khỏe mạnh."
    }
    return {"reports": [report]}
