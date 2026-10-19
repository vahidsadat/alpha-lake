from databricks import sql
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def get_financial_report(ticker : str, years : list[int]) -> pd.DataFrame:

    if not years:
        raise ValueError("Years parameter is required.")

    if not all(isinstance(year, int) for year in years):
        raise ValueError("All years must be integers.")
    years = sorted(set(years))  # Remove duplicates and sort the years

    placeholders = ', '.join(f":year_{i}" for i in range(len(years)))
    parameters = {"ticker": ticker}

    parameters.update({f"year_{i}": year for i, year in enumerate(years)})

    query =f"""
                    SELECT ticker, period_date, revenue, net_income, net_profit_margin FROM alphalake.gold.v_company_financials_report
                    WHERE ticker = :ticker AND YEAR(period_date) IN ({placeholders})
                    LIMIT 100
                    """
    with sql.connect(
            server_hostname = os.getenv("DATABRICKS_HOST"),
            http_path = os.getenv("HTTP_PATH"),
            access_token = os.getenv("DATABRICKS_ACCESS_TOKEN")
        ) as connection:
    
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                parameters = parameters
            )

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = cursor.fetchall()

    return pd.DataFrame(rows, columns=columns)