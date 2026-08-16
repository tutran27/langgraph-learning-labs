from langgraph.graph import StateGraph, START, END
from state import TravelState
from nodes import (
    vehicle_booking,
    hotel_booking,
    itinerary_planning,
)

builder = StateGraph(TravelState)

builder.add_node("vehicle_booking", vehicle_booking)
builder.add_node("hotel_booking", hotel_booking)
builder.add_node("itinerary_planning", itinerary_planning)

builder.add_edge(START, "vehicle_booking")
builder.add_edge("vehicle_booking", "hotel_booking")
builder.add_edge("hotel_booking", "itinerary_planning")
builder.add_edge("itinerary_planning", END)

graph = builder.compile()
