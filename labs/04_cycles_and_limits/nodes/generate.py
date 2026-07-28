import re
from shared.models import GroqLLMModel

try:
    from state import CodeWriterState
except ImportError:
    from ..state import CodeWriterState

def clean_code(content: str) -> str:
    match = re.search(r"```python\s*(.*?)\s*```", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    match_plain = re.search(r"```\s*(.*?)\s*```", content, re.DOTALL)
    if match_plain:
        return match_plain.group(1).strip()
        
    return content.strip()

def generate_code_node(state: CodeWriterState):
    model = GroqLLMModel()
    
    task_description = state['task_description']

    prompt = f"""You are an expert Python assistant.
Your task is to write a single, self-contained Python function that satisfies the following requirements:
<TASK>
{task_description}
</TASK>

CRITICAL INSTRUCTIONS:
1. Return ONLY the valid Python code block enclosed in ```python and ```.
2. Do NOT include any explanations, introductory text, or markdown formatting outside of the Python code block.
3. Do NOT include any test case executions, `assert` statements, or example function calls (e.g. `print(is_palindrome(...))`) inside or at the bottom of the code. We will execute and verify your function dynamically.
4. Make sure to import any necessary modules (e.g. `re`, `math`, `collections`) at the top of your code block.
5. Ensure the function name and signature match exactly what is described in the task.
"""

    response = model.invoke(prompt)
    code = clean_code(response.content)
            
    return {
        "code": code,
        "attempts": 0,
        "is_correct": False,
        "feedback": "Initial code generated."
    }

if __name__ == "__main__":
    demo_init_state = CodeWriterState(
        task_description="Write a Python function 'fibonacci_sequence(n)' that takes an integer n as input and returns a list of the first n Fibonacci numbers. The sequence starts with 0 and 1. If n is less than or equal to 0, return an empty list. If n is 1, return [0]. If n is 2, return [0, 1]. For n > 2, return the list of the first n Fibonacci numbers.",
    )
    
    result = generate_code_node(demo_init_state)
    print("Generated Code:\n", result['code'])