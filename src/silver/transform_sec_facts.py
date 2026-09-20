from pathlib import Path
from pyspark.sql import SparkSession, functions

spark = SparkSession.builder.appName(
    name="AlphaLake"
).getOrCreate()

def read_json(ticker:str):
    path = Path(f"data/bronze/sec/{ticker.upper()}/companyfacts.json")

    df_spark = (spark.read.option("multiline","true").json(str(path)))

    df_spark.printSchema()
    selected_df = df_spark.select(
        functions.explode("facts.us-gaap.AccountsPayableCurrent.units.USD").alias("observation")
    )
    
    selected_df.select("observation.*").show()
read_json("MSFT")