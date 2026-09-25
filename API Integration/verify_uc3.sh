#!/bin/bash
echo " Part 1: API Loader "
python3 loader.py

echo "Part 2: Schema Check "
docker exec -it pg-local psql -U postgres -d mydb -c "\dt"

echo " Part 3: Business Report (Revenue by Month)"
docker exec -it pg-local psql -U postgres -d mydb -c "
SELECT DATE_TRUNC('month', o.order_date) AS month, SUM(oi.quantity * oi.price) AS revenue
FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY 1 ORDER BY 1;"

echo " Part 4: Self-Join Hierarchy "
docker exec -it pg-local psql -U postgres -d mydb -c "
SELECT e.name AS employee, m.name AS manager
FROM employees e LEFT JOIN employees m ON e.manager_id = m.employee_id;"
