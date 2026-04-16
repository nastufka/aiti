select nomenclature_client.id, nomenclature_client.name, sum(np.price * n.quantity)
from nomenclature_client
         left join public.nomenclature_order no on nomenclature_client.id = no.client_id
         left join public.nomenclature_orderitem n on no.id = n.order_id
         left join public.nomenclature_product np on n.product_id = np.id
group by nomenclature_client.id, nomenclature_client.name;

select nomenclature_category.id, nomenclature_category.name, count(n_c.id)
from nomenclature_category
         left join nomenclature_category n_c on n_c.p_category_id = nomenclature_category.id
group by nomenclature_category.id, nomenclature_category.name
order by nomenclature_category.id;


CREATE OR REPLACE VIEW top_5_products_last_month AS
SELECT p.name,
       case when parent_cat.name is null then c.name else parent_cat.name end,
       SUM(nomenclature_orderitem.quantity) AS total_quantity
FROM nomenclature_orderitem
         JOIN nomenclature_order o ON o.id = nomenclature_orderitem.order_id
         JOIN nomenclature_product p ON p.id = nomenclature_orderitem.product_id
         LEFT JOIN nomenclature_category c ON c.id = p.category_id
         LEFT JOIN nomenclature_category parent_cat ON parent_cat.id = c.p_category_id
WHERE o.created_at >= NOW() - INTERVAL '1 month'
GROUP BY p.name, parent_cat.name, c.name
ORDER BY total_quantity DESC
LIMIT 5;