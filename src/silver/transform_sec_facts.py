from pathlib import Path
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName(
    name="AlphaLake"
).getOrCreate()

def transform_sec_facts(path: Path,ticker:str):
    raw_df = spark.read.text(
        str(path),
        wholetext=True)
    
    variant_df = raw_df.select( F.parse_json("value").alias("document") )
    us_gaap_df = variant_df.select(F.variant_get(F.col("document"),"$.facts['us-gaap']","variant").alias("us_gaap"))
    concept_df = us_gaap_df.lateralJoin(spark.tvf.variant_explode((F.col("us_gaap")).outer()).alias("concept"))
    units_df = concept_df.select(F.variant_get(F.col("concept.value"),"$.units","variant").alias("units_info"), "concept.key")
    observations_info_df = units_df.lateralJoin(spark.tvf.variant_explode((F.col("units_info")).outer()).alias("observations_info"))
    observations_info_df = observations_info_df.select(F.col("concept.key").alias( "concept"),F.col("observations_info.key").alias( "unit"), F.col("observations_info.value").alias( "observations"))
    observations_df = observations_info_df.lateralJoin(spark.tvf.variant_explode((F.col("observations")).outer()).alias("observations_attr"))
    fields_df = observations_df.select(
        F.lit(ticker).alias("ticker"),"concept", "unit",
        F.variant_get(F.col("observations_attr.value"),"$.accn","string").alias("accession_number"),
        F.variant_get(F.col("observations_attr.value"),"$.start","date").alias("period_start_date"),
        F.variant_get(F.col("observations_attr.value"),"$.end","date").alias("period_end_date"),
        F.variant_get(F.col("observations_attr.value"),"$.filed","date").alias("filing_date"),
        F.variant_get(F.col("observations_attr.value"),"$.form","string").alias("filing_form"),
        F.variant_get(F.col("observations_attr.value"),"$.fp","string").alias("fiscal_period"),
        F.variant_get(F.col("observations_attr.value"),"$.frame","string").alias("reporting_frame"),
        F.variant_get(F.col("observations_attr.value"),"$.fy","bigint").alias("fiscal_year"),
        F.variant_get(F.col("observations_attr.value"),"$.val","decimal(38,10)").alias("value")
        )
    return fields_df