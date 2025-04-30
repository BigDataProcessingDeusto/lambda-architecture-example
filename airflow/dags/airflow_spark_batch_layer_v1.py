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
        "retries": 1,
        "retry_delay": timedelta(minutes=5)
    },
    schedule="*/1 * * * *",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["example", "TGVD"],
) as dag:
    bash_task = BashOperator(
        task_id="rm_output",
        bash_command="rm -rf /opt/spark/work-dir/spark-batch-output/output"
    )

    submit_job = SparkSubmitOperator(
        application="/opt/airflow/spark/spark-batch-layer.py", task_id="submit_job"
    )

    bash_task >> submit_job

