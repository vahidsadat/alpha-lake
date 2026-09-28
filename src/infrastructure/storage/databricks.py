from src.gold.company_fundamentals import annual_derived_metrics, annual_cash_flow_metrics
from src.silver.transform_sec_facts import transform_sec_facts
from pyspark.sql import SparkSession
from pathlib import Path
from pyspark.sql import DataFrame
import json

# Bronze: writing fact in data folder in databricks
def save_company_facts_into_databricks(ticker: str, data:dict):
    path = Path(f"/Volumes/alphalake/raw/data/bronze/sec/{ticker.upper()}/companyfacts.json")

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data,f, indent=2)


# Silver: write the financial facts into Databricks
def write_financial_facts(ticker:str):
    path = Path(f"/Volumes/alphalake/raw/data/bronze/sec/{ticker}/companyfacts.json")
    table_name = "alphalake.silver.financial_facts"
    data_path = path
    df = transform_sec_facts(data_path, ticker)
    spark = df.sparkSession
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

def write_multi_financial_facts(tickers: list[str]):
    for ticker in tickers:
        try:
            write_financial_facts(ticker)
        except:
            continue
def write_company_financials(df, table_name = "alphalake.gold.company_financials"):
    spark = df.sparkSession
    spark.sql("CREATE NAMESPACE IF NOT EXISTS alphalake.gold")
    if not spark.catalog.tableExists(table_name):
        df.writeTo(table_name).using("delta").create()
    else:
        target_df = spark.table(table_name)
        source = df.alias("source")
        target = target_df.alias("target")
        comparison_df = source.join(
            target,
            (source.ticker == target.ticker)
            & (source.period_date == target.period_date),
            "left"
        )
        same_values = (
            source.revenue.eqNullSafe(target.revenue)
            & source.net_income.eqNullSafe(target.net_income)
            & source.operating_income.eqNullSafe(target.operating_income)
            & source.assets.eqNullSafe(target.assets)
            & source.equity.eqNullSafe(target.equity)
            & source.operating_margin.eqNullSafe(target.operating_margin)
            & source.net_profit_margin.eqNullSafe(target.net_profit_margin)
            & source.return_on_assets.eqNullSafe(target.return_on_assets)
            & source.return_on_equity.eqNullSafe(target.return_on_equity)
            & source.operating_cash_flow.eqNullSafe(target.operating_cash_flow)
            & source.operating_cash_flow_source.eqNullSafe(target.operating_cash_flow_source)
            & source.capex.eqNullSafe(target.capex)
            & source.capex_source.eqNullSafe(target.capex_source)
            & source.free_cash_flow.eqNullSafe(target.free_cash_flow)
        )
        changed_df = comparison_df.filter(
            target.ticker.isNull()| ~same_values
        ).select("source.*")
        if not(changed_df.isEmpty()):
            changed_df.createOrReplaceTempView("incoming_company_financials")
            spark.sql("""MERGE INTO alphalake.gold.company_financials AS target
            USING incoming_company_financials AS source
            ON target.ticker = source.ticker
            AND target.period_date = source.period_date
            WHEN MATCHED 
            THEN
                UPDATE SET *
            WHEN NOT MATCHED THEN
                INSERT *
            """)
        else:
            print("no changes detected")
        spark.sql(
                f"DESCRIBE HISTORY {table_name}"
            ).show(truncate=False)