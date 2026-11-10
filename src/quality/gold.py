from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def validate_gold (df: DataFrame) -> None:

    if df.isEmpty():
        raise ValueError("DataFrame is empty")

    null_key = (df.filter(F.col("ticker").isNull() | F.col("period_date").isNull())| F.col("fiscal_year").isNull()).limit(1)
    if not null_key.isEmpty():
        raise ValueError("DataFrame contains null values in key columns: 'ticker' or 'period_date'")

    duplicates = (
        df.groupBy("ticker", "period_date")
        .count()
        .filter(F.col("count") > 1)
        .limit(1)
    )
    duplicates_fy = (
            df.groupBy("ticker", "fiscal_year")
            .count()
            .filter(F.col("count") > 1)
            .limit(1)
        )

    if (not duplicates.isEmpty()) or (duplicates_fy.isEmpty()):
        raise ValueError(
            "Gold quality check failed: duplicate ticker + period_date or ticker + fiscal_year found"
        )

    difference_fiscal_endyear = F.year("period_date") - F.col("fiscal_year")
    bad_offset = df.filter(~difference_fiscal_endyear.isin([0,1])).limit(1)
    if not bad_offset.isEmpty:
        raise ValueError(
            "Gold quality check failed: fiscal_year must equal the period end year or the end year minus 1"
        )