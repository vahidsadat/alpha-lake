from company_fundamentals import annual_derived_metrics
from cash_flow_metrics import annual_cash_flow_metrics
from pathlib import Path
from pyspark.sql import SparkSession

path = Path("data/gold/sec/company_financials")
def write_company_financials(ticker:str):
    df = annual_derived_metrics(ticker)
    cash_flow_df = annual_cash_flow_metrics(ticker)
    df = df.join(cash_flow_df, ["ticker", "period_date"], "left")
    path.parent.mkdir(parents=True, exist_ok=True)
    spark = df.sparkSession
    spark.conf.set(
        "spark.sql.sources.partitionOverwriteMode",
        "dynamic"
    )
    df.write.partitionBy("ticker").mode("overwrite").parquet(str(path))

write_company_financials("AAPL")