from pyspark.sql import  DataFrame, functions as F




def safe_positive_ratio(numerator, denominator):
    return F.when(F.col(denominator).isNull() | (F.col(denominator) <= 0),F.lit(None)).otherwise(F.col(numerator)/F.col(denominator))

def cash_flow_quality(df:DataFrame):
    df = df.withColumn("capex_to_operating_cash_flow", safe_positive_ratio("capex","operating_cash_flow"))
    df = df.withColumn("free_cash_flow_conversion", safe_positive_ratio("free_cash_flow","operating_cash_flow"))

    return df.select(
    "ticker",
    "period_date",
    "capex_to_operating_cash_flow",
    "free_cash_flow_conversion")


