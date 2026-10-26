from datetime import datetime

from airflow import DAG
from airflow.providers.common.sql.hooks.handlers import fetch_all_handler
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from analys_for_month.tasks.truncate_monthly import truncate_monthly_sales
from analys_for_month.tasks.upload_data_to_monthly import upload_to_monthly_sales

CLICKHOUSE_CONN_ID = "clickhouse_default"

with DAG(
    dag_id='truncate_and_upload_monthly_sales',
    start_date=datetime(2026, 10, 23),
    default_args={"conn_id": CLICKHOUSE_CONN_ID},
    schedule="*/1 * * * *",
    catchup=False,
) as dag:
    truncate = truncate_monthly_sales()
    upload = upload_to_monthly_sales()

    truncate >> upload