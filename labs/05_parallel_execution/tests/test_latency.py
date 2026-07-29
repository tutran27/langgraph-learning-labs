import sys
import os
import pytest
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import graph

@pytest.mark.asyncio
async def test_parallel_execution_speed():
    start = time.perf_counter()
    await graph.ainvoke({"company": "NVDA", "reports": []})
    elapsed = time.perf_counter() - start
    
    assert elapsed < 2.0, f"Expected parallel execution < 2.0s, got {elapsed:.2f}s"
