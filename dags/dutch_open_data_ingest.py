from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.bootstrap_ingest import main

with DAG(
    dag_id="dutch_open_data_ingest",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    PythonOperator(task_id="bootstrap_ingest", python_callable=main)
