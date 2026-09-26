from pathlib import Path
from pyspark.sql import SparkSession, DataFrame, functions as F
from pyspark.sql.window import Window



def get_path():
    return Path("data/silver/sec/financial_facts")

def read_from_parquet():
    spark = SparkSession.builder.appName("AnnualCashFlow").getOrCreate()
    df = spark.read.parquet(str(get_path()))
    return df

def desire_ticker(ticker:str):
    df = read_from_parquet()
    ticker_df = df.filter(df.ticker == ticker)
    return ticker_df

def annual_duration_metrics_report(metric:str, output_name:str, df:DataFrame):
    
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
        F.col("value").alias(output_name)
        
    )
    return final_report_df

def canonical_metric(df:DataFrame,output_name:str,preferred_metric:str,fallback_metric:str):
    preferred_df = annual_duration_metrics_report(preferred_metric,output_name, df).withColumn(f"{output_name}_source", F.lit(preferred_metric))
    fallback_df = annual_duration_metrics_report(fallback_metric,output_name, df).withColumn( f"{output_name}_source", F.lit(fallback_metric))
    missing_fallback_df = fallback_df.join(
        preferred_df.select("ticker", "period_date"), ["ticker", "period_date"], "left_anti")
    final_df = preferred_df.unionByName(missing_fallback_df)
    return final_df


def annual_cash_flow_metrics(df:DataFrame) -> DataFrame:
    capex_df = canonical_metric(df,"capex", "PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets")
    operating_cf_df = canonical_metric(df,"operating_cash_flow", "NetCashProvidedByUsedInOperatingActivities", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations")
    free_cash_flow_df = operating_cf_df.join(capex_df, ["ticker", "period_date"], "left").withColumn("free_cash_flow", F.col("operating_cash_flow") - F.col("capex")).orderBy(["ticker", "period_date"])
    return free_cash_flow_df
if __name__ == "__main__":
    df = read_from_parquet()
    annual_cash_flow_metrics(df)
