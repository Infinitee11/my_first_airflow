from datetime import datetime

from airflow import DAG
from airflow.providers.common.sql.hooks.handlers import fetch_all_handler
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from create_orders.tasks import insert_orders

CLICKHOUSE_CONN_ID = "clickhouse_default"

with DAG(
    dag_id="create_orders",
    start_date=datetime(2026, 10, 23),
    default_args={"conn_id": CLICKHOUSE_CONN_ID},
    schedule="*/1 * * * *",
    catchup=False,
) as dag:
    insert_orders()

