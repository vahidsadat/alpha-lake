from pathlib import Path
import os
from src.ingestion.sec.sec_client import get_company_facts
from src.infrastructure.storage.local import save_company_facts
from src.infrastructure.storage.databricks import save_company_facts_into_databricks



def load_financials(tickers : list[str]):
    os.environ.setdefault("ALPHALAKE_ENV", "databricks")
    os.environ.setdefault("name", "Sadat Vahid")
    os.environ.setdefault("email", "sadatvahid1372@gmail.com")
    destination = os.getenv("ALPHALAKE_ENV", "local")
    for ticker in tickers:
        df = get_company_facts(ticker)
        if (destination == "local"):
            save_company_facts(ticker,df)
        elif (destination == 'databricks'):
            save_company_facts_into_databricks(ticker,df)
        else:
            ValueError("No destination has been chosen")

load_financials(["AAPL", "MSFT"])