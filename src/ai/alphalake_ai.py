
from openai import OpenAI
from databricks import sql
import os
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()

def get_financial_report(ticker : str, years : list[int]) -> pd.DataFrame:

    if not years:
        raise ValueError("Years parameter is required.")

    if not all(isinstance(year, int) for year in years):
        raise ValueError("All years must be integers.")
    years = sorted(set(years))  # Remove duplicates and sort the years

    placeholders = ', '.join(f":year_{i}" for i in range(len(years)))
    parameters = {"ticker": ticker}

    parameters.update({f"year_{i}": year for i, year in enumerate(years)})

    query =f"""
                    SELECT ticker, period_date, revenue, net_income, net_profit_margin FROM alphalake.gold.v_company_financials_report
                    WHERE ticker = :ticker AND YEAR(period_date) IN ({placeholders})
                    LIMIT 100
                    """
    with sql.connect(
            server_hostname = os.getenv("DATABRICKS_HOST"),
            http_path = os.getenv("HTTP_PATH"),
            access_token = os.getenv("DATABRICKS_ACCESS_TOKEN")
        ) as connection:
    
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                parameters = parameters
            )

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = cursor.fetchall()

    return pd.DataFrame(rows, columns=columns)


tools = [
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

# financial_df = get_financial_report("AAPL", 2025)
# print("\nColumns:")
# print(financial_df.columns.tolist())

# print("\nNumber of records:")
# print(len(financial_df))

# print("\nFinancial data:")
# print(financial_df.to_string(index=False))

# if financial_df.empty:
#     raise ValueError("No financial data found for the specified ticker.")
# financial_context = financial_df.to_json(
# orient = "records",
# date_format = "iso"
# )

client = OpenAI(
    base_url = "http://localhost:11434/v1",
    api_key = "ollama"
)

system_prompt = """
           You are AlphaLake AI.

For questions about company financial figures,
always retrieve the required data using an
available financial tool before answering.

Never answer financial questions using your
pretrained knowledge.

If the tool returns no data, explain that
the requested information is unavailable.
"""
messages = [
            {"role": "system", "content" : system_prompt}
        ]
print(get_financial_report(
    "AAPL",
    [2020, 2022, 2025]
))
while True:

    input_prompt = input("Enter your question (or type 'exit' to quit): ")
    if input_prompt.lower() == 'exit':
        break
    # analytic_prompt = f"""
                
    # What was Apple's net profit margin in fiscal year 2025?
    #             """
    messages.append({"role": "user", "content": input_prompt})
    analize = client.chat.completions.create(
        model = "qwen3:4b-instruct",
        messages = messages,
        tools = tools,
        tool_choice="required",
        temperature = 0
    )
    assistant_message = analize.choices[0].message
    messages.append(assistant_message)
    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            function_name =tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            ticker= arguments.get("ticker")
            years= arguments.get("years")
            print("Tool arguments:", arguments)
            if isinstance(years, int):
                years = [years]
            if function_name == "get_financial_report":
                analysis_result = get_financial_report(ticker, years).to_json(
                    orient = "records",
                    date_format = "iso"
                )
            else:
                raise ValueError(
                    f"Unknown function requested: {function_name}"
                )
            
            messages.append(
                {"role": "tool",
                "tool_call_id": tool_call.id,
                "content": analysis_result}
            )
            final_response = client.chat.completions.create(
                model="qwen3:4b-instruct",
                messages=messages
            )
            print(final_response.choices[0].message.content)
            final_message = final_response.choices[0].message

            messages.append(final_message)
            
    else:
        print("model response:", assistant_message.content)
