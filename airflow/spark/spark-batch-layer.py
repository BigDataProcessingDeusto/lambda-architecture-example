from pyspark.sql import SparkSession
import pyspark.sql.functions as f

spark = SparkSession \
    .builder \
    .appName("pizza-orders-batch-spark") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.json('/opt/spark/work-dir/filesink/')
df.printSchema()
df = df.select(f.col("payload.*"))

df = df.select("coupon_code", "date", "status", "store_id", "store_order_id", f.explode("order_lines"))
df = df.select("coupon_code", "date", "status", "store_id", "store_order_id", f.col("col.*"))

df.write.orc("/opt/work-dir/spark-batch-output/output/")
