TOOLS = [
    {
        "type": "function",
        "function":{
            "name": "get_financial_report",
            "description": "Retrieve financial report data for a given company ticker and fiscal year.",
            "parameters": {
                "type": "object",
                "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company."
                },
                "years": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "description": "The fiscal year(s) for which to retrieve the financial report."
                },
                },
                "required": ["ticker", "years"]
    
        },
    },
    }
]