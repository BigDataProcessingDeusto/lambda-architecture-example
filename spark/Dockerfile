FROM spark:3.5.5

ADD spark-speed-layer-v3.py /opt/spark/work-dir/

ENTRYPOINT ["sh", "-c", "/opt/spark/bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 4 --conf spark.jars.ivy=/opt/spark/work-dir/ --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 /opt/spark/work-dir/spark-speed-layer-v3.py"]