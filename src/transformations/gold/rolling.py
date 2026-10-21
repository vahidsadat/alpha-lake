from pyspark.sql import DataFrame, functions as F
from pyspark.sql.window import Window



def add_rolling_metrics(df:DataFrame, metrics, year):
    return df.withColumn(f"{metrics}_3y_avg", F.avg(F.col(metrics)).over(year))


def rolling_metrics(df: DataFrame)->DataFrame:
    window = Window.partitionBy("ticker").orderBy("period_date").rowsBetween(-2,0)
    df = add_rolling_metrics(df,"operating_cash_flow",window)
    df = add_rolling_metrics(df,"free_cash_flow",window)
    final_result_df = df.select(
        "ticker",
        "period_date",
        "operating_cash_flow_3y_avg",
        "free_cash_flow_3y_avg"
    )

    return final_result_df


