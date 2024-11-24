import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            car_id INTEGER PRIMARY KEY,
            model TEXT,
            available INTEGER,
            price_per_day REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            rental_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            car_id INTEGER,
            rental_date TEXT,
            return_date TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY(car_id) REFERENCES cars(car_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            rental_id INTEGER,
            amount REAL,
            payment_date TEXT,
            FOREIGN KEY(rental_id) REFERENCES rentals(rental_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance (
            maintenance_id INTEGER PRIMARY KEY,
            car_id INTEGER,
            description TEXT,
            date TEXT,
            FOREIGN KEY(car_id) REFERENCES cars(car_id)
        )
    """)

    conn.commit()
    conn.close()

# Run database initialization
init_db()
