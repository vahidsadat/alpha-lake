from pyspark.sql import DataFrame
from ..transformations.gold.fundamentals import annual_derived_metrics
from ..transformations.gold.cash_flow import annual_cash_flow_metrics
from ..transformations.gold.cash_flow_quality import cash_flow_quality
from ..transformations.gold.growth import annual_growth_metrics
from ..transformations.gold.rolling import rolling_metrics
from ..storage.gold import write_company_financials , write_cash_flow_quality_metrics, write_growth_metrics, write_rolling_metrics
from ..quality.gold import validate_gold

def run_gold(silver_df: DataFrame, destination: str):
    fundamental_df = annual_derived_metrics(silver_df)
    cash_flow_df = annual_cash_flow_metrics(silver_df)

    gold_df = fundamental_df.join(
        cash_flow_df, ["ticker","period_date"], "left"
    )
    validate_gold(gold_df)
    print("Gold data quality checks passed.")
    write_company_financials(gold_df, destination)
    cash_flow_quality_df = cash_flow_quality(gold_df)
    growth_metrics_df =  annual_growth_metrics(gold_df)
    rolling_metrics_df = rolling_metrics(gold_df)
    write_cash_flow_quality_metrics(cash_flow_quality_df, destination)
    write_growth_metrics(growth_metrics_df,destination)
    write_rolling_metrics(rolling_metrics_df,destination)