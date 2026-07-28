import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routers import route_input

def test_route_input_text():
    state = {"input_type": "text"}
    assert route_input(state) == "process_text"

def test_route_input_number():
    state = {"input_type": "number"}
    assert route_input(state) == "process_number"

def test_route_input_unsupported():
    state = {"input_type": "unsupported"}
    assert route_input(state) == "reject"
