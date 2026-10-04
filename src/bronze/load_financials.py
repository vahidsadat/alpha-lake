import argparse
from pathlib import Path
import os
from src.ingestion.sec.sec_client import get_company_facts
from src.infrastructure.storage.local import save_company_facts
from src.infrastructure.storage.databricks import save_company_facts_into_databricks
from databricks.sdk import WorkspaceClient



def load_financials(tickers : list[str],name:str,email:str):
    destination = os.getenv("ALPHALAKE_ENV", "local")
    for ticker in tickers:
        df = get_company_facts(ticker,name,email)
        if (destination == "local"):
            save_company_facts(ticker,df)
        elif (destination == 'databricks'):
            save_company_facts_into_databricks(ticker,df)
        else:
            raise ValueError("No destination has been chosen")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--env",
        default="databricks",
    )

    parser.add_argument(
        "--name",
        required=True,
    )

    parser.add_argument(
        "--email",
        required=True,
    )

    args = parser.parse_args()

    os.environ["ALPHALAKE_ENV"] = args.env

    load_financials(["AAPL", "MSFT"],
        args.name,
        args.email,)