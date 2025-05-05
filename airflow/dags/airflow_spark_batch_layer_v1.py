from airflow.models import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

with DAG(
    dag_id="spark_batch_layer_v1",
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 0,
        "retry_delay": timedelta(minutes=5)
    },
    schedule="*/10 * * * *",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["example", "TGVD"],
) as dag:
    bash_task = BashOperator(
        task_id="rm_output",
        bash_command="rm -rf /opt/spark/work-dir/spark-batch-output/output"
    )

    spark_conf = {
        "spark.jars.ivy": "/opt/airflow/",
        "spark.jars.packages": "org.apache.hadoop:hadoop-aws:3.3.4",
        "spark.hadoop.fs.s3a.access.key": "minio-root-user",
        "spark.hadoop.fs.s3a.secret.key": "minio-root-password",
        "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
        "spark.hadoop.fs.s3a.path.style.access": "true"
    }

    submit_job = SparkSubmitOperator(
        application="/opt/airflow/spark/spark-batch-layer.py", task_id="submit_job",
        packages="org.apache.hadoop:hadoop-aws:3.3.4,org.apache.hadoop:hadoop-common:3.3.4",
        conf=spark_conf
    )

    bash_task >> submit_job

