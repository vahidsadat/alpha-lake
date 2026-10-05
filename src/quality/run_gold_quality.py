from pyspark.sql import SparkSession

from src.quality.gold_quality import validate_gold


def main():
    spark = SparkSession.builder.getOrCreate()

    gold_df = spark.table("alphalake.gold.company_financials")

    validate_gold(gold_df)

    print("Gold data quality checks passed.")


if __name__ == "__main__":
    main()