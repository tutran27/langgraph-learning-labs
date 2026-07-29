import sys
import os
import asyncio
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import graph
from nodes.financial_analysis import financial_analysis_node
from nodes.risk_analysis import risk_analysis_node
from nodes.technical_analysis import technical_analysis_node
from nodes.synthesize import synthesize_node

async def run_sequential(company: str):
    start = time.perf_counter()
    state = {"company": company, "reports": []}
    
    res1 = await financial_analysis_node(state)
    state["reports"].extend(res1["reports"])
    
    res2 = await risk_analysis_node(state)
    state["reports"].extend(res2["reports"])
    
    res3 = await technical_analysis_node(state)
    state["reports"].extend(res3["reports"])
    
    synthesize_node(state)
    return time.perf_counter() - start

async def run_parallel(company: str):
    start = time.perf_counter()
    result = await graph.ainvoke({"company": company, "reports": []})
    return time.perf_counter() - start, result

async def main():
    print("=" * 60)
    print("BENCHMARK: SEQUENTIAL VS PARALLEL EXECUTION")
    print("=" * 60)
    
    print("\n1. Running Sequential...")
    seq_time = await run_sequential("AAPL")
    print(f"⏱️ Sequential Time: {seq_time:.2f}s")
    
    print("\n2. Running Parallel via LangGraph...")
    par_time, result = await run_parallel("AAPL")
    print(f"⏱️ Parallel Time:   {par_time:.2f}s")
    
    print("-" * 60)
    print(f"📊 Speedup: {seq_time / par_time:.1f}x faster using parallel execution in LangGraph!")
    print("=" * 60)
    print("\n[FINAL REPORT]:")
    print(result["final_summary"])

if __name__ == "__main__":
    asyncio.run(main())
