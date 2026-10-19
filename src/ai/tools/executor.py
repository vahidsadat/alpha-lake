from .financials import get_financial_report


TOOL_FUNCTIONS = {
    "get_financial_report": get_financial_report}

def execute_tool(function_name:str, arguments:dict):
    if function_name not in TOOL_FUNCTIONS:
        raise ValueError(f"Unknown function requested: {function_name}")
    tool_function = TOOL_FUNCTIONS[function_name]
    return tool_function(**arguments)
    