import requests

api_url = "https://www.sec.gov/files/company_tickers.json"

def get_company_tickers(name:str,email:str):

    headers = {
    "User-Agent": f"{name} {email}",
    "Accept-Encoding": "gzip, deflate"
    }

    response = requests.get(api_url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    return(data)

def get_CIK(ticker:str,name:str,email:str):

    ticker = ticker.upper()

    for company in get_company_tickers(name,email).values():
        if ticker == company["ticker"].upper():
            return str(company["cik_str"]).zfill(10)

    raise ValueError(f"Ticker is not found:{ticker}")
