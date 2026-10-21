from pathlib import Path
import json
from pyspark.sql import SparkSession
from .path import STORAGE_PATH


# Bronze: writing fact in data folder
def save_company_facts(ticker: str, data:dict , destination: str):
    path = Path(f"{STORAGE_PATH[destination]['bronze']}/{ticker.upper()}/companyfacts.json")

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data,f, indent=2)

def read_bronze(spark: SparkSession, ticker: str, destination: str):
    path = f"{STORAGE_PATH[destination]['bronze']}/{ticker.upper()}/companyfacts.json"
    return spark.read.text(
        path, wholetext= True
    )
