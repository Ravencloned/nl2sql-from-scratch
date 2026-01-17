import sqlite3
from pathlib import Path

# -----------------------------
# Create data directory
# -----------------------------
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

db_path = data_dir / "sample.db"

# -----------------------------
# Connect to SQLite
# -----------------------------
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# -----------------------------
# Create schema + insert data
# -----------------------------
cursor.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    country TEXT NOT NULL,
    signup_date TEXT NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    payment_method TEXT NOT NULL,
    payment_status TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

INSERT INTO customers VALUES
(1, 'Alice Johnson', 'alice@example.com', 'USA', '2023-01-10'),
(2, 'Bob Smith', 'bob@example.com', 'India', '2023-02-15'),
(3, 'Charlie Lee', 'charlie@example.com', 'USA', '2023-03-20'),
(4, 'Diana Patel', 'diana@example.com', 'India', '2023-04-05'),
(5, 'Ethan Brown', 'ethan@example.com', 'UK', '2023-05-12');

INSERT INTO products VALUES
(1, 'Laptop', 'Electronics', 800.00),
(2, 'Smartphone', 'Electronics', 500.00),
(3, 'Headphones', 'Accessories', 150.00),
(4, 'Office Chair', 'Furniture', 300.00),
(5, 'Coffee Machine', 'Appliances', 250.00);

INSERT INTO orders VALUES
(1, 1, '2023-06-01', 'COMPLETED'),
(2, 2, '2023-06-05', 'COMPLETED'),
(3, 3, '2023-06-10', 'PENDING'),
(4, 1, '2023-06-15', 'COMPLETED'),
(5, 4, '2023-06-20', 'COMPLETED');

INSERT INTO order_items VALUES
(1, 1, 1, 1, 800.00),
(2, 1, 3, 2, 150.00),
(3, 2, 2, 1, 500.00),
(4, 3, 5, 1, 250.00),
(5, 4, 4, 1, 300.00),
(6, 5, 2, 2, 500.00);

INSERT INTO payments VALUES
(1, 1, 'Credit Card', 'SUCCESS', 1100.00),
(2, 2, 'UPI', 'SUCCESS', 500.00),
(3, 4, 'Credit Card', 'SUCCESS', 300.00),
(4, 5, 'Debit Card', 'SUCCESS', 1000.00);
""")

conn.commit()
conn.close()

print(f"✅ SQLite database created at: {db_path.resolve()}")
