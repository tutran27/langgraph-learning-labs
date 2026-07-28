from shared.models import GroqLLMModel
from .generate import clean_code

try:
    from state import CodeWriterState
except ImportError:
    from ..state import CodeWriterState

def revise_code_node(state: CodeWriterState):
    model = GroqLLMModel()
    
    task_description = state['task_description']
    buggy_code = state['code']
    feedback = state['feedback']
    attempts = state.get('attempts', 0) + 1
    
    print(f"--- [Node] revise_code_node: Revision Attempt {attempts} ---")
    
    prompt = f"""You are an expert Python assistant.
Your previous Python code failed testing. Your task is to analyze the error feedback and modify the code so that it passes all tests.

<TASK_DESCRIPTION>
{task_description}
</TASK_DESCRIPTION>

<BUGGY_CODE>
{buggy_code}
</BUGGY_CODE>

<ERROR_FEEDBACK>
{feedback}
</ERROR_FEEDBACK>

Please return ONLY the corrected Python code block (enclosed in ```python and ```).
Do not include any explanations, markdown comments, or introductory text outside of the code block.
Ensure the function name and arguments remain consistent with the requirements.
"""

    response = model.invoke(prompt)
    revised_code = clean_code(response.content)
    
    return {
        "code": revised_code,
        "attempts": attempts,
        "is_correct": False,
        "feedback": f"Revised code generated (attempt {attempts})."
    }
