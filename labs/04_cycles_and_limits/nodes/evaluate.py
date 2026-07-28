import traceback
import re

try:
    from state import CodeWriterState
except ImportError:
    from ..state import CodeWriterState

def evaluate_code_node(state: CodeWriterState):
    code = state.get("code", "")
    test_cases = state.get("test_cases", [])
    
    print(f"--- [Node] evaluate_code_node: Running tests ---")
    
    attempts = state.get("attempts", 0)
    max_attempts = state.get("max_attempts", 3)

    def make_fail_response(feedback_msg: str):
        stop_reason = "max_attempts_reached" if attempts >= max_attempts else None
        return {
            "is_correct": False,
            "feedback": feedback_msg,
            "stop_reason": stop_reason
        }

    if not code.strip():
        return make_fail_response("No code was generated.")
        
    local_env = {}
    try:
        exec(code, local_env)
        
        print("--- [Debug] local_env keys & values ---")
        for k, v in local_env.items():
            if k != "__builtins__":
                print(f"  - Key '{k}': Type = {type(v).__name__}, Value = {v}")
    except Exception as e:
        error_msg = f"Syntax or compilation error during load:\n{traceback.format_exc()}"
        return make_fail_response(error_msg)
        
    func_name = None
    match = re.search(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)
    if match:
        func_name = match.group(1)
        
    if not func_name or func_name not in local_env or not callable(local_env[func_name]):
        callables = [k for k, v in local_env.items() if callable(v)]
        if callables:
            func_name = callables[0]
        else:
            return make_fail_response("Could not find any callable function in the generated code.")
            
    func = local_env[func_name]
    
    for idx, tc in enumerate(test_cases):
        inputs = tc.get("input")
        expected = tc.get("expected")
        
        if isinstance(inputs, tuple):
            args = inputs
        elif isinstance(inputs, list):
            args = (inputs,)
        else:
            args = (inputs,)
            
        try:
            result = func(*args)
            if result != expected:
                feedback_msg = (
                    f"Test Case {idx+1} Failed!\n"
                    f"Function call: {func_name}{args}\n"
                    f"Expected: {expected} (type: {type(expected).__name__})\n"
                    f"Got: {result} (type: {type(result).__name__})"
                )
                return make_fail_response(feedback_msg)
            else:
                print("------------- [Debug] Test Case Passed --------------  ")
                print(f"Test Case {idx+1} Passed!")
                print(f"Function call: {func_name}{args}")
                print(f"Expected: {expected} (type: {type(expected).__name__})")
                print(f"Got: {result} (type: {type(result).__name__})")
                
        except Exception as e:
            feedback_msg = (
                f"Exception raised during Test Case {idx+1} execution:\n"
                f"Function call: {func_name}{args}\n"
                f"Error: {str(e)}\n"
                f"Traceback:\n{traceback.format_exc()}"
            )
            return make_fail_response(feedback_msg)
            
    return {
        "is_correct": True,
        "feedback": "All tests passed!",
        "stop_reason": "success"
    }

if __name__ == "__main__":
    code = """
def fibonacci_sequence(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        sequence = [0, 1]
        while len(sequence) < n:
            sequence.append(sequence[-1] + sequence[-2])
        return sequence
    """
    test_cases = [
        {"input": 5, "expected": [0, 1, 1, 2, 3]},
        {"input": 1, "expected": [0]},
        {"input": 2, "expected": [0, 1]},
        {"input": 0, "expected": []}
    ]
    
    input_init = CodeWriterState(
        code=code,
        test_cases=test_cases,
        attempts=0,
        max_attempts=3,
        is_correct=False,
        stop_reason=None
    )
    result = evaluate_code_node(input_init)
    print(result)