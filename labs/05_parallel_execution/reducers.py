from typing import Dict, Any

def merge_analysis_dicts(left: Dict[str, Any], right: Dict[str, Any]) -> Dict[str, Any]:
    merged = left.copy() if left else {}
    merged.update(right)
    return merged
