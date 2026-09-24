import pytest
from pathlib import Path
from src.silver.transform_sec_facts import transform_sec_facts
from pyspark.sql import functions as F
import decimal

@pytest.fixture(scope="module")
def df():
    data_path = Path("tests/fixtures/companyfacts_sample.json")
    return transform_sec_facts(data_path,"AAPL")

def test_column_names(df):
    expected_columns = [
        "ticker",
        "concept",
        "unit",
        "accession_number",
        "period_start_date",
        "period_end_date",
        "filing_date",
        "filing_form",
        "fiscal_period",
        "reporting_frame",
        "fiscal_year",
        "value",
    ]
    assert df.columns == expected_columns, f"Expected columns: {expected_columns}, but got: {df.columns}"

def test_data_types(df):
    expected_data_types = {
        "ticker": "string",
        "concept": "string",
        "unit": "string",
        "accession_number": "string",
        "period_start_date": "date",
        "period_end_date": "date",
        "filing_date": "date",
        "filing_form": "string",
        "fiscal_period": "string",
        "reporting_frame": "string",
        "fiscal_year": "bigint",
        "value": "decimal(38,10)",
    }
    actual_data_types = {field.name: field.dataType.simpleString() for field in df.schema.fields}
    assert actual_data_types == expected_data_types, f"Expected data types: {expected_data_types}, but got: {actual_data_types}"

def test_ticker_name(df):
    assert df.select("ticker").distinct().collect()[0][0] == "AAPL", "Ticker name should be 'AAPL'"

def test_asset_fact_start_date(df):
    assets_df = df.filter(df.concept == "Assets")
    assert assets_df.count() > 0, "No Assets records found"
    assert assets_df.filter(F.col("period_start_date").isNull()).count() == assets_df.count(), "Assets records should have null period_start_date"

def test_revenue_fact_start_date_end(df):
    revenue_df = df.filter(df.concept == "RevenueFromContractWithCustomerExcludingAssessedTax")
    assert revenue_df.count() > 0, "No Revenue records found"
    assert revenue_df.filter(F.col("period_end_date").isNull()).count() == 0 , "All Revenue records should not have null period_end_date"
    assert revenue_df.filter(F.col("period_start_date").isNull()).count() == 0, "All Revenue records should not have null period_start_date"

def test_EPS_decimal(df):
    df_eps = df.filter(df.concept == "EarningsPerShareBasic")
    assert df_eps.count() > 0, "No EarningsPerShareBasic records found"
    value = df_eps.select("value").first()["value"]
    assert value == decimal.Decimal(str(6.11)), "EarningsPerShareBasic value should be 6.11"