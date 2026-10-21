from pyspark.sql import SparkSession
from ..storage.bronze import read_bronze
from ..transformations.silver.sec_facts import transform_sec_facts
from ..storage.silver import write_financial_facts

def run_silver(spark: SparkSession, tickers: list[str], destination: str):
    for ticker in tickers:
        ticker = ticker.upper()
        bronze_df = read_bronze(spark, ticker, destination)
        silver_df = transform_sec_facts(bronze_df, spark, ticker)
        write_financial_facts(silver_df, ticker, destination)
        

    