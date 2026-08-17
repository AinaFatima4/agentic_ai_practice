import json

from agents import function_tool
import json   
from datetime import datetime  
from logger import logger


@function_tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression and return the result. Use this for any arithmetic, for example '47 * 89' or '(5 + 3) / 2'."""

    logger.info(f"TOOL SELECTED: calculator | INPUT: {expression}")
    result_value = eval(expression)                 # turns the text "47 * 89" into the number 4183

    logger.info(f"TOOL RESULT: calculator | OUTPUT: {result_value}")
    return str(result_value)



#tool to get the current date and time 
@function_tool
def get_current_time() -> str:
    """Return the current system date and time. Use this whenever the user asks what the date or time is."""
    logger.info("TOOL SELECTED: get_current_time")

    now = datetime.now()                                    # grab the current moment
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")      # turn it into readable text

    logger.info(f"TOOL RESULT: get_current_time | OUTPUT: {formatted_time}")
    return formatted_time


#tool to looksup employee information from the json file
@function_tool
def get_employee_info(employee_name: str) -> str:
    """Look up an employee's department and role by their name. Use this for questions about a specific employee."""

    logger.info(f"TOOL SELECTED: get_employee_info | INPUT: {employee_name}")

    # open and read the JSON file into a Python list of dicts
    with open("employees.json", "r") as file:

        employees = json.load(file)

    # search for a matching employee (case-insensitive so "ayesha khan" matches "Ayesha Khan")
    for employee in employees:
        if employee["name"].lower() == employee_name.lower():
            result = f"{employee['name']} works in the {employee['department']} department as a {employee['role']}."
            logger.info(f"TOOL RESULT: get_employee_info | OUTPUT: {result}")
            return result

    not_found = f"No employee named '{employee_name}' was found."
    logger.info(f"TOOL RESULT: get_employee_info | OUTPUT: {not_found}")
    return not_found



#tool to search the knowledge base for relevant documents based on a query
@function_tool
def search_knowledge_base(query: str):
    query_words = query.lower().split()

    with open("employees.json", "r", encoding="utf-8") as f:
        documents = json.load(f)
    logger.info(f"TOOL SELECTED: search_knowledge_base | INPUT: {query}")

    results = []

    for document in documents:
        text = json.dumps(document).lower()

        score = sum(word in text for word in query_words)

        if score > 0:
            results.append((score, document))

    results.sort(reverse=True, key=lambda x: x[0])

    logger.info(f"TOOL OUTPUT: search_knowledge_base | OUTPUT: {results[:5]}")
    
    return [document for score, document in results[:5]]