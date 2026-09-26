from .transform_sec_facts import transform_sec_facts
from pathlib import Path
from pyspark.sql import SparkSession


def get_bronze_path(ticker: str):
    return Path(f"data/bronze/sec/{ticker}/companyfacts.json")
def write_financial_facts(ticker:str):
    silver_path = Path("data/silver/sec/financial_facts")
    data_path = get_bronze_path(ticker)
    df = transform_sec_facts(data_path, ticker)
    silver_path.parent.mkdir(parents=True, exist_ok=True)
    spark = df.sparkSession
    spark.conf.set(
            "spark.sql.sources.partitionOverwriteMode",
            "dynamic"
        )
    df.write.partitionBy("ticker").mode("overwrite").parquet(str(silver_path))

def write_multi_financial_facts(tickers: list[str]):
    for ticker in tickers:
        try:
            write_financial_facts(ticker)
        except:
            continue

write_multi_financial_facts(["AAPL","MSFT"])