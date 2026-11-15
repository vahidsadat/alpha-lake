import requests
import os
from src.db.connection import PostgresClient
from src.db.companies import CompanyRepository


print("creating client...")
client = PostgresClient()
print("connected")
company = CompanyRepository(client=client)
name = os.getenv("SEC_NAME")
email = os.getenv("SEC_EMAIL")
def get_companies():
    HEADERS = {
        "User-Agent": f"{name} {email}",
        "Accept-Encoding": "gzip, deflate"
        }
    api_url = "https://www.sec.gov/files/company_tickers_exchange.json"
    response = requests.get(api_url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("data")

def run_pipeline():
    company.create_table()
    list_companies = get_companies()
    company.add_companies(list_companies)

run_pipeline()
