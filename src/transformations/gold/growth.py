from pyspark.sql import DataFrame, functions as F
from pyspark.sql.window import Window




def add_growth_yoy(df:DataFrame, metrics:list[str])-> DataFrame:
    growth_df = df
    annual_partition = Window.partitionBy(
            "ticker"
        ).orderBy("period_date")
    previous_year = F.lag(F.col("period_date")).over(annual_partition)
    is_previous_year = (F.year("period_date") - F.year(previous_year) == 1)
    for metric in metrics:
        previous_value = F.lag(F.col(metric)).over(annual_partition)

        if metric.lower() != "revenue":
            growth_df = growth_df.withColumn(f"{metric}_growth_yoy",F.when(
                ~is_previous_year | previous_value.isNull() | (previous_value <= 0), F.lit(None)
            ).otherwise((F.col(metric) - previous_value) / previous_value  ))
        else:
            growth_df = growth_df.withColumn(f"{metric}_growth_yoy",F.when(
                ~is_previous_year, F.lit(None)
            ).otherwise((F.col(metric) - previous_value) / previous_value  ))

    return growth_df
    

def annual_growth_metrics(df: DataFrame):
    report_df = add_growth_yoy(df, metrics=["operating_cash_flow","free_cash_flow"])
    final_df = report_df.select("ticker", "period_date", "operating_cash_flow_growth_yoy", "free_cash_flow_growth_yoy")

    return final_df



    

