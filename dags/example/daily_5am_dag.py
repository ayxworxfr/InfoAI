from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "email": ["example@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# 每天凌晨5点运行
with DAG(
    "daily_5am_dag",
    default_args=default_args,
    description="A simple DAG that runs every day at 5 AM",
    schedule_interval="0 5 * * *",
    catchup=False,
) as dag:

    start_task = DummyOperator(task_id="start_task")

    processing_task = DummyOperator(task_id="processing_task")

    end_task = DummyOperator(task_id="end_task")

    start_task >> processing_task >> end_task

