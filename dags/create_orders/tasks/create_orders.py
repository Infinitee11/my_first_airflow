import clickhouse_connect
from data_engineering_workflow.utils.noob_nuke import query_from_file
from random import randint, choice
from datetime import date
from airflow.decorators import task
from data_engineering_workflow.utils.noob_nuke import insert

@task
def insert_orders():
    with clickhouse_connect.get_client(
        host="clickhouse",
        port=8123,
        username="default",
        password="changeme",
        database='ruslan',
    ) as client:
        last_id = client.query(query_from_file(__file__, 'get_last_id'))
        last_order, last_order_items = last_id.result_rows[0]
        customers_id = client.query(query_from_file(__file__, 'customers_id'))
        products_id_and_prices = client.query(query_from_file(__file__, 'products_id'))
        prices = dict(products_id_and_prices.result_rows)
        stores = client.query(query_from_file(__file__, 'stores_id'))

        status = ['delivered', 'placed', 'cancelled']
        for _ in range(randint(1, 100)):
            last_order += 1
            total_amount = 0

            for _ in range(randint(1, 10)):
                last_order_items += 1
                product = choice(products_id_and_prices.result_rows)[0]
                price = prices[product]
                quantity = randint(1,5)
                new_order_item = [
                    [last_order_items, 
                    last_order, 
                    product, 
                    quantity, 
                    price]
                ]
                total_amount += price * quantity
                client.insert(
                    "order_items",
                    new_order_item,
                    column_names=["order_item_id", "order_id", 'product_id', 'quantity', 'price_at_purchase']
                )

            new_order = [
                [last_order, 
                choice(customers_id.result_rows)[0], 
                choice(stores.result_rows)[0], 
                date.today(), 
                choice(status), 
                total_amount]
            ]
            client.insert(
                "orders",
                new_order,
                column_names=["order_id", "customer_id", 'store_id', 'order_date', 'status', 'total_amount']
                )
            

