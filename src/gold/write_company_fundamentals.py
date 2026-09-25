from company_fundamentals import annual_derived_metrics
from pathlib import Path

path = Path("data/gold/sec/company_fundamentals")
def write_company_fundamentals(ticker:str):
    df = annual_derived_metrics(ticker)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write.mode("overwrite").parquet(str(path))

write_company_fundamentals("AAPL")