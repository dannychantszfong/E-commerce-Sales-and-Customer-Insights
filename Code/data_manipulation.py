import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('E-commerce Sales and Customer Insights\Data\olist.sqlite')

# Define the queries
queries = {
    "Total Revenue": """
    SELECT SUM(oi.price) AS total_revenue
    FROM order_items oi;
    """,
    "Monthly Sales Trend": """
    SELECT STRFTIME('%Y-%m', o.order_purchase_timestamp) AS month, 
           SUM(oi.price) AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY month
    ORDER BY month;
    """,
    "Top 10 Best-Selling Products": """
    SELECT p.product_id, 
           COUNT(oi.order_id) AS total_orders, 
           SUM(oi.price) AS total_revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id
    ORDER BY total_orders DESC
    LIMIT 10;
    """,
    "Top 5 Product Categories by Sales": """
    SELECT c.product_category_name_english, 
           COUNT(oi.order_id) AS total_orders, 
           SUM(oi.price) AS total_revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN product_category_name_translation c 
    ON p.product_category_name = c.product_category_name
    GROUP BY c.product_category_name_english
    ORDER BY total_revenue DESC
    LIMIT 5;
    """,
    "Most Valuable Customers": """
    SELECT c.customer_id, 
           SUM(oi.price) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id
    ORDER BY total_spent DESC
    LIMIT 10;
    """,
    "Customer Purchase Frequency": """
    SELECT c.customer_id, 
           COUNT(o.order_id) AS total_orders, 
           AVG(oi.price) AS average_order_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id
    ORDER BY total_orders DESC;
    """,
    "Average Delivery Time": """
    SELECT AVG(JULIANDAY(o.order_delivered_customer_date) - JULIANDAY(o.order_purchase_timestamp)) AS avg_delivery_time
    FROM orders o
    WHERE o.order_delivered_customer_date IS NOT NULL;
    """,
    "Payment Methods Usage": """
    SELECT payment_type, 
           COUNT(payment_type) AS count
    FROM order_payments
    GROUP BY payment_type
    ORDER BY count DESC;
    """
}

# Execute the queries and store the results in a dictionary
results = {}
for key, query in queries.items():
    df = pd.read_sql_query(query, conn)
    results[key] = df

# Close the database connection
conn.close()

# Display the results
for key, df in results.items():
    print(f"\nResults for: {key}")
    print(df)

# Optional: Save results to CSV files
for key, df in results.items():
    df.to_csv(f"{key}.csv", index=False)
