from edgar import Company, set_identity
from dotenv import load_dotenv
import os

load_dotenv()

set_identity(f"{os.getenv('name')} {os.getenv('email')}")


company = Company("MSFT")
financials = company.get_financials()
income_statement = financials.income_statement()

print (income_statement)