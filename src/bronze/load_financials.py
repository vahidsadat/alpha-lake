from pathlib import Path
import os
from src.ingestion.sec.sec_client import get_company_facts
from src.infrastructure.storage.local import save_company_facts
from src.infrastructure.storage.databricks import save_company_facts_into_databricks


destination = os.getenv("ALPHALAKE_ENV", "local")
def load_financials(tickers : list[str]):
    for ticker in tickers:
        try:
            df = get_company_facts(ticker)
            if (destination == "local"):
                save_company_facts(ticker,df)
            elif (destination == 'databricks'):
                save_company_facts_into_databricks
            else:
                ValueError("No destination has been chosen")
        except:
            continue

load_financials(["AAPL", "MSFT"])