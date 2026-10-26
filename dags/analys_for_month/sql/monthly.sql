select formatDateTime(o.order_date, '%Y-%m') as sales_month,
count(o.order_id) as total_orders,
sum(
case
	when o.status = 'delivered'
	then 1
	else 0
end
) as delivered_orders,
sum(
case
	when o.status = 'cancelled'
	then 1
	else 0
end
) as cancelled_orders,
sum(
case
	when o.status = 'delivered'
	then o.total_amount
	else 0
end
) as revenue,
round(
        100.0 * cancelled_orders / nullIf(total_orders, 0),
        2
    ) AS cancellation_rate
from orders as o
GROUP BY formatDateTime(o.order_date, '%Y-%m')
order by sales_month 