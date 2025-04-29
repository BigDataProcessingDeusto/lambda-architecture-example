from pyspark.sql import SparkSession
import pyspark.sql.functions as f

spark = SparkSession \
    .builder \
    .appName("pizza-orders-spark") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Create a streaming DataFrame
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-server:9092") \
    .option("subscribe", "pizza-orders") \
    .load()
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "CAST(timestamp AS TIMESTAMP)")

df = df.select(f.get_json_object(df.key, "$.payload").alias("key"),
	f.get_json_object(df.value, "$.payload").alias("value"), df.timestamp)

json_schema = f.schema_of_json('{"store_id":7,"store_order_id":11160,"coupon_code":1695,"date":18979,"status":"accepted","order_lines":[{"product_id":85,"category":"salad","quantity":3,"unit_price":11.83,"net_price":35.49}]}')

df = df.select(df.key, f.from_json(df.value, json_schema).alias("value"), df.timestamp)
df = df.select(df.key, df.timestamp, f.col("value.*"))
df = df.filter(df.status == "accepted")
df = df.select(df.key, df.timestamp, df.coupon_code, df.status, df.store_id, df.store_order_id, f.explode("order_lines").alias("order_lines"))
df = df.select(df.key, df.timestamp, df.coupon_code, df.status, df.store_id, df.store_order_id, f.col("order_lines.*"))

df = df.select(df.key, df.timestamp, df.store_id, df.store_order_id, df.net_price).groupBy("key", "timestamp", "store_id", "store_order_id").sum("net_price")


query = df.selectExpr("CAST(key AS STRING) AS key", "CAST(to_json(struct(*)) AS STRING) AS value", "CAST(timestamp AS STRING) as timestamp") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-server:9092") \
    .option("topic", "pizza-live-stats") \
    .option("checkpointLocation", "/tmp/spark-checkpoint") \
    .outputMode("complete") \
    .start() 

query.awaitTermination()
