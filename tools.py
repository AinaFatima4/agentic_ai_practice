
from agents import function_tool


@function_tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression and return the result. Use this for any arithmetic, for example '47 * 89' or '(5 + 3) / 2'."""

    print("calculator called with:", expression)   

    result_value = eval(expression)                 # turns the text "47 * 89" into the number 4183

    print("calculator tool result:", result_value)       # so you see what it returns
    return str(result_value)