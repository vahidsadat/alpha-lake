import json
from pathlib import Path
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.window import Window
from silver.transform_sec_facts import transform_sec_facts



def get_path():
    return Path("data/silver/sec/financial_facts")

def read_from_parquet(path: Path):
    spark = SparkSession.builder.appName("AnnualCashFlow").getOrCreate()
    df = spark.read.parquet(str(path))
    return df

def desire_ticker(ticker:str):
    df = read_from_parquet(get_path())
    ticker_df = df.filter(df.ticker == ticker)
    return ticker_df

def annual_duration_metrics_report(ticker:str,metric:str, output_name:str):
    df = desire_ticker(ticker)
    report_df = df.filter(df.concept == metric)
    duration_diff = F.date_diff(F.col("period_end_date"), F.col("period_start_date"))
    report_df = report_df.withColumn("duration_diff", duration_diff)
    annual_report_df = report_df.filter((F.col("duration_diff") > 350) & (F.col("duration_diff") < 380))
    annual_partition = Window.partitionBy(
        "ticker",
        "concept",
        "unit",
        "period_start_date",
        "period_end_date",
    ).orderBy(F.col("filing_date").desc())
    annual_report_df = annual_report_df.withColumn("row_number", F.row_number().over(annual_partition)).filter(F.col("row_number") == 1)
    final_report_df = annual_report_df.select(
        F.col("ticker"),
        F.col("period_end_date").alias("period_date"),
        F.col("value").alias(output_name),
    )
    return final_report_df

annual_duration_metrics_report("AAPL","NetCashProvidedByUsedInOperatingActivities","operating_cash_flow").show(20, truncate=False)

