from src.gold.company_fundamentals import annual_derived_metrics, annual_cash_flow_metrics
from pathlib import Path
from pyspark.sql import DataFrame


def write_company_financials(df: DataFrame):
    path = Path("data/gold/sec/company_financials")
    derived_report_df = annual_derived_metrics(df)
    cash_flow_df = annual_cash_flow_metrics(df)
    final_report_df = derived_report_df.join(cash_flow_df, ["ticker", "period_date"], "left")
    path.parent.mkdir(parents=True, exist_ok=True)
    spark = final_report_df.sparkSession
    spark.conf.set(
        "spark.sql.sources.partitionOverwriteMode",
        "dynamic"
    )
    final_report_df\
        .write.partitionBy("ticker")\
        .mode("overwrite")\
        .parquet(str(path))