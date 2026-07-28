from typing import Dict

def merge_checklist(left: Dict[str, bool], right: Dict[str, bool]) -> Dict[str, bool]:
    merged = left.copy()
    merged.update(right)
    return merged