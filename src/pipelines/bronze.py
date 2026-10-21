import argparse
from src.ingestion.sec.client import get_company_facts
from ..storage.bronze import save_company_facts



def run_bronze(tickers : list[str],name:str,email:str, destination: str):
    for ticker in tickers:
        data = get_company_facts(ticker,name,email)
        save_company_facts(ticker,data, destination)

def main():

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


    run_bronze(["AAPL", "MSFT"],
        args.name,
        args.email,
        args.env)

if __name__ == "__main__":
    main()
    