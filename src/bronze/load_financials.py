from pathlib import Path
import json
from src.ingestion.sec.sec_client import get_company_facts


def save_company_facts(ticker: str, data:dict):
    path = Path(f"data/bronze/sec/{ticker.upper()}/companyfacts.json")

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data,f, indent=2)

ticker = "AAPL"
save_company_facts(ticker,get_company_facts(ticker))