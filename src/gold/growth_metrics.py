from pathlib import Path
from pyspark.sql import SparkSession, DataFrame, functions as F
from pyspark.sql.window import Window



def get_path():
    return Path("data/gold/sec/company_financials")

def read_from_parquet():
    spark = SparkSession.builder.appName("AnnualCashFlow").getOrCreate()
    df = spark.read.parquet(str(get_path()))
    return df

def desire_ticker(ticker:str):
    df = read_from_parquet(get_path())
    ticker_df = df.filter(df.ticker == ticker)
    return ticker_df

def add_growth_yoy(df:DataFrame, metrics:list[str])-> DataFrame:
    growth_df = df
    annual_partition = Window.partitionBy(
            "ticker"
        ).orderBy("period_date")
    for metric in metrics:
        previous_value = F.lag(F.col(metric)).over(annual_partition)

        if metric.lower() != "revenue":
            growth_df = growth_df.withColumn(f"{metric}_growth_yoy",F.when(
                previous_value.isNull() | (previous_value <= 0), F.lit(None)
            ).otherwise((F.col(metric) - previous_value) / previous_value  ))
        else:
            growth_df = growth_df.withColumn(f"{metric}_growth_yoy", (F.col(metric) - previous_value) / previous_value )

    return growth_df

def annual_growth_metrics(df: DataFrame):
    report_df = add_growth_yoy(df, metrics=["operating_cash_flow","free_cash_flow"])
    final_df = report_df.select("ticker", "period_date", "operating_cash_flow_growth_yoy", "free_cash_flow_growth_yoy")

    return final_df

def write_growth_metrics(df:DataFrame):
    path = Path("data/gold/sec/growth_metrics")
    path.parent.mkdir(parents=True, exist_ok=True)
    spark = df.sparkSession
    spark.conf.set(
        "spark.sql.sources.partitionOverwriteMode",
        "dynamic"
    )
    df.write.partitionBy("ticker").mode("overwrite").parquet(str(path))

df = read_from_parquet()
write_growth_metrics(df)

    

