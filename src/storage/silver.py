from pathlib import Path
from pyspark.sql import SparkSession, DataFrame, functions as F
from .path import STORAGE_PATH



def write_financial_facts(df: DataFrame, ticker: str, destination: str):
    spark = df.sparkSession
    if destination == "local":
        silver_path = Path(f"{STORAGE_PATH[destination]['silver']}/financial_facts")
        silver_path.parent.mkdir(parents=True, exist_ok=True)
        
        spark.conf.set(
                "spark.sql.sources.partitionOverwriteMode",
                "dynamic"
            )
        df.write.partitionBy("ticker").mode("overwrite").parquet(str(silver_path))
    elif destination == "databricks":
        table_name = STORAGE_PATH[destination]['silver']
        spark.sql(
            "CREATE SCHEMA IF NOT EXISTS alphalake.silver"
        )
        if not spark.catalog.tableExists(table_name):
            (
                df.writeTo(table_name)
                .using("delta")
                .partitionedBy("ticker")
                .create()
            )
        else:
            (
                df.write
                .format("delta")
                .mode("overwrite")
                .option(
                    "replaceWhere",
                    f"ticker = '{ticker}'"
                )
                .saveAsTable(table_name)
            )
    else:
        raise ValueError(f"Unknown destination: {destination}")

def read_silver(spark: SparkSession, destination: str , ticker: str | None = None):
    if destination == "local":
        df= spark.read.parquet(
            f"{STORAGE_PATH[destination]['silver']}/financial_facts"
        )
    elif destination == "databricks":
        df= spark.read.table(
                    STORAGE_PATH[destination]['silver']
                )
    else:
        raise ValueError(f"Unknown destination: {destination}")

    if ticker:
        ticker = ticker.upper()
        df = df.filter(F.col("ticker") == ticker)
    return df