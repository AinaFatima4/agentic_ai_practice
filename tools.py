
from agents import function_tool
import json   



@function_tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression and return the result. Use this for any arithmetic, for example '47 * 89' or '(5 + 3) / 2'."""

    print("calculator called with:", expression)   

    result_value = eval(expression)                 # turns the text "47 * 89" into the number 4183

    print("calculator tool result:", result_value)       # so you see what it returns
    return str(result_value)





@function_tool
def get_employee_info(employee_name: str) -> str:
    """Look up an employee's department and role by their name. Use this for questions about a specific employee."""

    print("get_employee_info called with:", employee_name)

    # open and read the JSON file into a Python list of dicts
    with open("employees.json", "r") as file:

        employees = json.load(file)

    # search for a matching employee (case-insensitive so "ayesha khan" matches "Ayesha Khan")
    for employee in employees:
        if employee["name"].lower() == employee_name.lower():
            result = f"{employee['name']} works in the {employee['department']} department as a {employee['role']}."
            print("get_employee_info result:", result)
            return result

    not_found = f"No employee named '{employee_name}' was found."
    print("get_employee_info result:", not_found)
    return not_found