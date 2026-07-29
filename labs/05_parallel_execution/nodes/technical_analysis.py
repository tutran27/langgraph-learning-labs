import asyncio
from state import AnalysisState

async def technical_analysis_node(state: AnalysisState):
    company = state.get("company", "N/A")
    print(f"  --> [Technical Analysis] Analyzing {company}...")
    await asyncio.sleep(1.0)
    
    report = {
        "type": "technical",
        "title": "Technical Indicators",
        "details": f"Giá của {company} nằm trên đường MA50, chỉ số RSI cho thấy xu hướng tăng (Bullish)."
    }
    return {"reports": [report]}
