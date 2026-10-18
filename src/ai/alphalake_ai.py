from openai import OpenAI

client = OpenAI(
    base_url = "http://localhost:11434/v1",
    api_key = "ollama"
)
financial_data = {
    "company": "Microsoft",
    "revenue_2024": 100_000_000,
    "revenue_2025": 125_000_000
}

revenue_2024 = financial_data['revenue_2024']
revenue_2025 = financial_data['revenue_2025']
growth = ((revenue_2025 - revenue_2024) * 100) / revenue_2024
print("growth", f"{growth:.2f}%")

system_prompt = """
            You are AlphaLake AI, a financial research assistant.

            Rules:
            1. Use only the financial data provided by the application.
            2. Never invent financial figures.
            3. Do not speculate about business performance or
            revenue drivers without supporting evidence.
            4. Clearly distinguish facts from interpretations.
            5. If information is insufficient, explain what is missing.
            6. Keep your answers concise and professional.   
"""
analytic_prompt = f"""
            Company: {financial_data['company']}
            Revenue 2024: ${revenue_2024:,}
            Revenue 2025: ${revenue_2025:,}
            Growth: {growth:.2f}%

            Provide a factual financial summary.
             Do not speculate about reasons for the growth.
            """
analize = client.chat.completions.create(
    model = "qwen3:4b-instruct",
    messages = [
        {"role": "system", "content" : system_prompt},
        {"role": "user","content": analytic_prompt}
    ]
)
analysis_result = analize.choices[0].message.content
report = client.chat.completions.create(
    model="qwen3:4b-instruct",
    messages=[
        {
            "role": "system",
            "content": """
            You are a financial report writer.
            Use only the supplied analysis.
            Do not introduce new financial facts.
            """
        },
        {
            "role": "user",
            "content": f"""
            Convert the following analysis into
            a concise financial report.

            {analysis_result}
            """
        }
    ]
)

print(report.choices[0].message.content)