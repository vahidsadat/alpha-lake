from edgar import Company, set_identity
import requests
from dotenv import load_dotenv
import json
import os
from src.ingestion.sec.ticker_cik import get_CIK

load_dotenv()

HEADERS = {
    "User-Agent": f"{os.getenv('name')} {os.getenv('email')}",
    "Accept-Encoding": "gzip, deflate"
}

def get_company_facts(ticker:str):
    cik = get_CIK(ticker=ticker)
    api_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    response = requests.get(api_url, headers=HEADERS, timeout=30)
    data = response.json()
    return data
