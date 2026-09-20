import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_url = "https://www.sec.gov/files/company_tickers.json"

def get_company_tickers():

    headers = {
    "User-Agent": f"{os.getenv('name')} {os.getenv('email')}",
    "Accept-Encoding": "gzip, deflate"
    }

    response = requests.get(api_url, headers=headers)
    data = response.json()
    return(data)

def get_CIK(ticker:str):

    ticker = ticker.upper()

    for company in get_company_tickers().values():
        if ticker == company["ticker"].upper():
            return str(company["cik_str"]).zfill(10)

    raise ValueError(f"Ticker is not found:{ticker}")
