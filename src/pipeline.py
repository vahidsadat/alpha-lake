from bronze.load_financials import load_financials
from silver.write_financial_facts import write_multi_financial_facts
from gold import company_fundamentals, cash_flow_quality_metrics, growth_metrics,rolling_metrics


def run_pipeline(tickers: list[str]):
    load_financials(tickers)
    write_multi_financial_facts(tickers)

    silver_df = company_fundamentals.read_from_parquet()
    company_fundamentals.write_company_financials(silver_df)

    company_df = growth_metrics.read_from_parquet()

    growth_metrics.write_growth_metrics(company_df)
    cash_flow_quality_metrics.write_cash_flow_growth_metrics(company_df)
    rolling_metrics.write_rolling_metrics(company_df)


run_pipeline(["AAPL","MSFT"])