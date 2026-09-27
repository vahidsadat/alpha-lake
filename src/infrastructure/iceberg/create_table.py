from src.infrastructure.spark.session import get_spark_session
from pathlib import Path

spark = get_spark_session()

path = Path("data/gold/sec/company_financials")

df = spark.read.parquet(str(path))
spark.sql("CREATE NAMESPACE IF NOT EXISTS local.gold")
if not spark.catalog.tableExists("local.gold.company_financials"):
    df.writeTo("local.gold.company_financials").using("iceberg").create()
else:
    target_df = spark.table("local.gold.company_financials")
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
        spark.sql("""MERGE INTO local.gold.company_financials AS target
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
spark.sql("""
    SELECT
        committed_at,
        snapshot_id,
        parent_id,
        operation,
        summary
    FROM local.gold.company_financials.snapshots
    ORDER BY committed_at
""").show(100,truncate=False)