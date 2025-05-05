from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import os

spark = SparkSession \
    .builder \
    .appName("pizza-orders-batch-spark") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

spark = SparkSession.builder \
    .appName("Batch processing") \
    .getOrCreate()

s3_input_path = "s3a://pizza-orders/topics/"
s3_output_path = "s3a://spark-batch-output/output"

df = spark.read.json(s3_input_path)

# df = df.select(f.col("payload.*"))

df = df.select("coupon_code", "date", "status", "store_id", "store_order_id", f.explode("order_lines"))
df = df.select("coupon_code", "date", "status", "store_id", "store_order_id", f.col("col.*"))

df.write.orc(s3_output_path)
