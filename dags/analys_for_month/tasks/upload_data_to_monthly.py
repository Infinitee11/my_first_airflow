import clickhouse_connect
from data_engineering_workflow.utils.noob_nuke import insert_as, truncate
from datetime import date
from airflow.decorators import task
from data_engineering_workflow.utils.noob_nuke import insert

table = 'mart_monthly_sales'
columns = ('sales_month',
            'total_orders',
            'delivered_orders',
            'cancelled_orders',
            'revenue',
            'cancellation_rate'
            )      


@task
def upload_to_monthly_sales():
    with clickhouse_connect.get_client(
        host="clickhouse",
        port=8123,
        username="default",
        password="changeme",
        database='ruslan',
    ) as client:
        sql = insert_as(__file__, table, columns, 'monthly')
        client.command(sql)