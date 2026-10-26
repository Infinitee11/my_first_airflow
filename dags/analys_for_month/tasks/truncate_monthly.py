import clickhouse_connect
from data_engineering_workflow.utils.noob_nuke import insert_as, truncate
from datetime import date
from airflow.decorators import task


table = 'mart_monthly_sales'

@task
def truncate_monthly_sales():
    with clickhouse_connect.get_client(
        host="clickhouse",
        port=8123,
        username="default",
        password="changeme",
        database='ruslan',
    ) as client:
        sql = truncate(table)
        client.command(sql)


