from transform_sec_facts import transform_sec_facts
from pathlib import Path

path = Path("data/silver/sec/financial_facts")
data_path = Path("data/bronze/sec/AAPL/companyfacts.json")
def write_financial_facts(data_path: Path, ticker:str):
    df = transform_sec_facts(data_path,ticker)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write.mode("overwrite").parquet(str(path))
    df.printSchema()
    df.show(5, truncate=False)

write_financial_facts(data_path,"AAPL")