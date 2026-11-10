# Databricks notebook source
from src.pipelines.bronze import run_bronze
from src.pipelines.silver import run_silver
from src.pipelines.gold import run_gold
from src.storage.silver import read_silver
from src.runtime.session import get_spark_session
# from databricks.sdk.runtime import dbutils
# dbutils.library.restartPython()

def run_pipeline():

    spark = get_spark_session()
    tickers = ["AAPL", "MSFT"]
    destination  = "databricks"
    dbutils.widgets.text("sec_name", "")
    dbutils.widgets.text("sec_email", "")

    name = dbutils.widgets.get("sec_name")
    email = dbutils.widgets.get("sec_email")
    if not name or not email:
        raise ValueError(
            "SEC_NAME and SEC_EMAIL must be configured."
        )
    run_bronze(tickers, name, email, destination)
    run_silver(spark,tickers,destination)
    silver_df = read_silver(spark=spark, destination=destination)
    run_gold(silver_df, destination)


run_pipeline()