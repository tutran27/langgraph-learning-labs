from state import AnalysisState

def synthesize_node(state: AnalysisState):
    company = state.get("company", "N/A")
    reports = state.get("reports", [])
    
    print(f"  --> [Synthesize] Merging {len(reports)} reports...")
    
    lines = [f"=== COMPREHENSIVE INVESTMENT REPORT FOR {company.upper()} ==="]
    for idx, r in enumerate(reports, 1):
        lines.append(f"{idx}. [{r['title']}]: {r['details']}")
    
    lines.append("===> KẾT LUẬN: KHUYẾN NGHỊ TÍCH LŨY CỔ PHIẾU.")
    final_text = "\n".join(lines)
    return {"final_summary": final_text}
