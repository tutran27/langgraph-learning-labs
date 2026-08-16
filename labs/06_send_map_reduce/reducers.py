from typing import List, Dict, Any

def merge_analyses(left: List[Dict[str, Any]], right: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged = left.copy() if left else []
    merged.extend(right)
    return merged
