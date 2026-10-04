from edgar import Company, set_identity
import requests
from src.ingestion.sec.ticker_cik import get_CIK




def get_company_facts(ticker:str,name:str, email:str):
    HEADERS = {
    "User-Agent": f"{name} {email}",
    "Accept-Encoding": "gzip, deflate"
    }
    cik = get_CIK(ticker=ticker, name=name,email=email)
    api_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    response = requests.get(api_url, headers=HEADERS, timeout=30)
    data = response.json()
    return data
