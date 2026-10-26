select
	max(o.order_id),
	max(oi.order_item_id)
from
	orders as o
join order_items as oi
on
	o.order_id = oi.order_id
