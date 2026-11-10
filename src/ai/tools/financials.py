from databricks import sql
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

ALLOWED_METRICS = {
    "revenue", "net_income", "operating_income", "net_profit_margin",
    "operating_margin", "return_on_assets", "return_on_equity",
    "operating_cash_flow", "capex", "free_cash_flow",
    "free_cash_flow_growth_yoy", "free_cash_flow_conversion",
}

def _run_query(query: str, parameters: dict) -> pd.DataFrame:
    with sql.connect(
        server_hostname=os.getenv("DATABRICKS_HOST"),
        http_path=os.getenv("HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_ACCESS_TOKEN")
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, parameters=parameters)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=columns)

def get_metrics(ticker : str, metrics: list[str], years : list[int] | None =None) -> pd.DataFrame:
    bad_requested_metrics = [metric for metric in metrics if metric not in ALLOWED_METRICS]
    if bad_requested_metrics:
        raise ValueError(f"Invalid metrics requested: {bad_requested_metrics}. Allowed metrics are: {ALLOWED_METRICS}")
    if not years:
        raise ValueError("Years parameter is required.")

    if not all(isinstance(year, int) for year in years):
        raise ValueError("All years must be integers.")
    years = sorted(set(years))  # Remove duplicates and sort the years

    placeholders = ', '.join(f":year_{i}" for i in range(len(years)))
    ticker = ticker.upper()
    parameters = {"ticker": ticker}

    parameters.update({f"year_{i}": year for i, year in enumerate(years)})
    selected_metrics = ', '.join(["ticker","period_date", *metrics])
    query =f"""
                    SELECT {selected_metrics} FROM alphalake.gold.v_company_financials_report
                    WHERE ticker = :ticker AND YEAR(period_date) IN ({placeholders})
                    ORDER BY period_date LIMIT 100
                    """
    

    return _run_query(query, parameters)