from typing import Annotated, List, Dict
from typing_extensions import TypedDict
import operator

from reducers import merge_checklist

class TravelState(TypedDict):
    input: str
    destination: str                   
    total_cost: Annotated[int, operator.add] 
    itinerary: Annotated[List[str], operator.add] 
    checklist: Annotated[Dict[str, bool], merge_checklist]
