import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import graph

@pytest.mark.asyncio
async def test_parallel_merge():
    input_state = {"company": "TSLA", "reports": []}
    result = await graph.ainvoke(input_state)
    
    assert len(result["reports"]) == 3
    report_types = {r["type"] for r in result["reports"]}
    assert report_types == {"financial", "risk", "technical"}
    assert "TSLA" in result["final_summary"]
