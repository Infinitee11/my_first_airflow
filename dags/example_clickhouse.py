from datetime import datetime

from airflow import DAG
from airflow.providers.common.sql.hooks.handlers import fetch_all_handler
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

CLICKHOUSE_CONN_ID = "clickhouse_default"
CLICKHOUSE_TABLE = "airflow_example"

with DAG(
    dag_id="example_clickhouse",
    start_date=datetime(2021, 1, 1),
    default_args={"conn_id": CLICKHOUSE_CONN_ID},
    schedule="@once",
    catchup=False,
) as dag:
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        sql=f"""
            CREATE TABLE IF NOT EXISTS {CLICKHOUSE_TABLE} (
                id   UInt32,
                name String,
                ts   DateTime DEFAULT now()
            ) ENGINE = MergeTree()
            ORDER BY id
        """,
    )

    insert_rows = SQLExecuteQueryOperator(
        task_id="insert_rows",
        sql=f"""
            INSERT INTO {CLICKHOUSE_TABLE} (id, name) VALUES
                (1, 'Alice'),
                (2, 'Bob'),
                (3, 'Charlie')
        """,
    )

    read_rows = SQLExecuteQueryOperator(
        task_id="read_rows",
        sql=f"SELECT id, name FROM {CLICKHOUSE_TABLE} ORDER BY id",
        handler=fetch_all_handler,
    )

    drop_table = SQLExecuteQueryOperator(
        task_id="drop_table",
        sql=f"DROP TABLE IF EXISTS {CLICKHOUSE_TABLE}",
    )

    create_table >> insert_rows >> read_rows >> drop_table