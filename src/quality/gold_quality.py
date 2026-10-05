from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def validate_gold (df: DataFrame) -> bool:

    if df.isEmpty():
        raise ValueError("DataFrame is empty")

    null_key = (df.filter(F.col("ticker").isNull() | F.col("period_date").isNull())).limit(1)
    if not null_key.isEmpty():
        raise ValueError("DataFrame contains null values in key columns: 'ticker' or 'period_date'")

    duplicates = (
        df.groupBy("ticker", "period_date")
        .count()
        .filter(F.col("count") > 1)
        .limit(1)
    )

    if not duplicates.isEmpty():
        raise ValueError(
            "Gold quality check failed: duplicate ticker + period_date found"
        )
