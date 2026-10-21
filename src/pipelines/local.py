import os
from dotenv import load_dotenv
from .bronze import run_bronze
from .silver import run_silver
from .gold import run_gold
from ..storage.silver import read_silver
from ..runtime.session import get_spark_session

load_dotenv()

def main():
    spark = get_spark_session()
    tickers = ["AAPL", "MSFT"]
    destination  = "local"
    name = os.getenv("SEC_NAME")
    email = os.getenv("SEC_EMAIL")
    if not name or not email:
        raise ValueError(
            "SEC_NAME and SEC_EMAIL must be configured."
        )
    run_bronze(tickers, name, email, destination)
    run_silver(spark,tickers,destination)
    silver_df = read_silver(spark=spark, destination=destination)
    run_gold(silver_df, destination)

if __name__ == "__main__":
    main()