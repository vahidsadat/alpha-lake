from pathlib import Path
from pyspark.sql import SparkSession, DataFrame, functions as F
from pyspark.sql.window import Window



def get_path():
    return Path("data/gold/sec/company_financials")

def read_from_parquet():
    spark = SparkSession.builder.appName("CashFlowQuality").getOrCreate()
    df = spark.read.parquet(str(get_path()))
    return df

def desire_ticker(ticker:str):
    df = read_from_parquet(get_path())
    ticker_df = df.filter(df.ticker == ticker)
    return ticker_df

def safe_positive_ratio(numerator, denominator):
    return F.when(F.col(denominator).isNull() | (F.col(denominator) <= 0),F.lit(None)).otherwise(F.col(numerator)/F.col(denominator))

def cash_flow_quality(df:DataFrame):
    df = df.withColumn("capex_to_operating_cash_flow", safe_positive_ratio("capex","operating_cash_flow"))
    df = df.withColumn("free_cash_flow_conversion", safe_positive_ratio("free_cash_flow","operating_cash_flow"))

    return df.select(
    "ticker",
    "period_date",
    "capex_to_operating_cash_flow",
    "free_cash_flow_conversion")

def write_cash_flow_growth_metrics(df: DataFrame):
    path = Path("data/gold/sec/cash_flow_quality")
    report_df = cash_flow_quality(df)
    path.parent.mkdir(parents=True, exist_ok=True)
    spark = report_df.sparkSession
    spark.conf.set(
        "spark.sql.sources.partitionOverwriteMode",
        "dynamic"
    )
    df.write.partitionBy("ticker").mode("overwrite").parquet(str(path))

df =read_from_parquet()
write_cash_flow_growth_metrics(df)