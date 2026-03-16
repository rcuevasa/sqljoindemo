import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect('joins_demo.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def create_tables(conn):
    """Create sample tables for join demonstrations"""
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            order_date TEXT,
            product_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            manager_id INTEGER,
            FOREIGN KEY (manager_id) REFERENCES employees(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL
        )
    """)

    conn.commit()

def insert_sample_data(conn):
    """Insert sample data for join demonstrations"""
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM users")

    # Insert users
    users = [
        (1, 'Alice', 'alice@example.com'),
        (2, 'Bob', 'bob@example.com'),
        (3, 'Charlie', 'charlie@example.com'),
        (4, 'Diana', 'diana@example.com'),
        (5, 'Eve', 'eve@example.com'),
    ]
    cursor.executemany("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", users)

    # Insert orders (note: Eve has no orders, Charlie has multiple)
    orders = [
        (1, 1, 100.00, '2024-01-01', 1),
        (2, 1, 250.50, '2024-01-15', 2),
        (3, 2, 75.25, '2024-01-10', 1),
        (4, 3, 300.00, '2024-01-05', 3),
        (5, 3, 150.00, '2024-01-20', 2),
        (6, 3, 200.00, '2024-02-01', 1),
        # Note: order 7 has a user_id that doesn't exist (orphan record)
        (7, 99, 50.00, '2024-01-25', 2),
    ]
    cursor.executemany("INSERT INTO orders (id, user_id, amount, order_date, product_id) VALUES (?, ?, ?, ?, ?)", orders)

    # Insert employees (with manager hierarchy)
    employees = [
        (1, 'Alice CEO', None),
        (2, 'Bob VP', 1),
        (3, 'Charlie Manager', 2),
        (4, 'Diana Manager', 2),
        (5, 'Eve Developer', 3),
        (6, 'Frank Developer', 3),
        (7, 'Grace Developer', 4),
    ]
    cursor.executemany("INSERT INTO employees (id, name, manager_id) VALUES (?, ?, ?)", employees)

    # Insert products
    products = [
        (1, 'Widget A', 50.00),
        (2, 'Widget B', 100.00),
        (3, 'Widget C', 150.00),
    ]
    cursor.executemany("INSERT INTO products (id, name, price) VALUES (?, ?, ?)", products)

    conn.commit()

def display_table(conn, table_name):
    """Display all rows from a table"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    print(f"\n{'='*60}")
    print(f"Table: {table_name.upper()}")
    print('='*60)

    if rows:
        # Print header
        headers = rows[0].keys()
        print(f"{' | '.join(headers)}")
        print('-' * 60)

        # Print data
        for row in rows:
            print(f"{' | '.join(str(v) for v in row)}")
    else:
        print("No data")

    print()

def main():
    """Setup the demonstration database"""
    print("Setting up SQL Joins Demonstration Database")
    print("="*60)

    with get_db_connection() as conn:
        create_tables(conn)
        insert_sample_data(conn)
        display_table(conn, 'users')
        display_table(conn, 'orders')
        display_table(conn, 'employees')
        display_table(conn, 'products')

    print("Database 'joins_demo.db' created successfully!")

if __name__ == '__main__':
    main()
