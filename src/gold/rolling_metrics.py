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

def add_rolling_metrics(df:DataFrame, metrics, year):
    return df.withColumn(f"{metrics}_3y_avg", F.avg(F.col(metrics)).over(year))


def rolling_metrics(df: DataFrame)->DataFrame:
    window = Window.partitionBy("ticker").orderBy("period_date").rowsBetween(-2,0)
    df = add_rolling_metrics(df,"operating_cash_flow",window)
    df = add_rolling_metrics(df,"free_cash_flow",window)
    final_result_df = df.select(
        "ticker",
        "period_date",
        "operating_cash_flow_3y_avg",
        "free_cash_flow_3y_avg"
    )

    return final_result_df

def write_rolling_metrics(df:DataFrame):
    path = Path("data/gold/sec/rolling_metrics")
    path.parent.mkdir(parents=True, exist_ok=True)
    spark = df.sparkSession
    spark.conf.set(
        "spark.sql.sources.partitionOverwriteMode",
        "dynamic"
    )
    df.write.partitionBy("ticker").mode("overwrite").parquet(str(path))



df = read_from_parquet()
write_rolling_metrics(df)