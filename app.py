import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import sqlite3
from datetime import datetime

is_admin = False

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


    # Add clean sample data
    cursor.execute("DELETE FROM cars WHERE car_id = 1")
    cursor.execute("DELETE FROM cars WHERE car_id = 2")
    cursor.execute("INSERT OR IGNORE INTO cars (car_id, model, available, price_per_day) VALUES (1, 'Toyota Corolla', 1, 50)")
    cursor.execute("INSERT OR IGNORE INTO cars (car_id, model, available, price_per_day) VALUES (2, 'Honda Civic', 1, 60)")

    cursor.execute("DELETE FROM customers WHERE customer_id = 1")
    cursor.execute("DELETE FROM customers WHERE customer_id = 2")
    cursor.execute("INSERT OR IGNORE INTO customers (customer_id, name, phone) VALUES (1, 'John Smith', '2703822346')")
    cursor.execute("INSERT OR IGNORE INTO customers (customer_id, name, phone) VALUES (2, 'Jane Doe', '7143895621')")

    conn.commit()
    conn.close()


# Run database initialization
init_db()


# Function to search for available cars
def view_cars():
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE available = 1")
    cars = cursor.fetchall()
    conn.close()

    if cars:
        result = "Available Cars:\n\n"
        for car in cars:
            result += f"Car ID: {car[0]}, Model: {car[1]}, Price per Day: ${car[3]}\n"
        messagebox.showinfo("View Cars", result)
    else:
        messagebox.showinfo("View Cars", "No cars available.")


# Function to book a car
def book_car():
    def submit_booking():
        car_id = car_id_entry.get()
        customer_name = customer_name_entry.get()
        customer_phone = customer_phone_entry.get()
        rental_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not car_id or not customer_name or not customer_phone:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = sqlite3.connect("car_rental.db")
        cursor = conn.cursor()


        # Check if the car is available
        cursor.execute("SELECT available FROM cars WHERE car_id = ?", (car_id,))
        car = cursor.fetchone()

        if car and car[0] == 1:
            # Add customer
            cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer_name, customer_phone))
            customer_id = cursor.lastrowid

            # Add rental
            cursor.execute("INSERT INTO rentals (customer_id, car_id, rental_date) VALUES (?, ?, ?)", (customer_id, car_id, rental_date))

            # Update car availability
            cursor.execute("UPDATE cars SET available = 0 WHERE car_id = ?", (car_id,))
            conn.commit()
            messagebox.showinfo("Success", "Car booked successfully!")
        else:
            messagebox.showerror("Error", "Car is not available.")
        
        conn.close()
        booking_window.destroy()

    booking_window = tk.Toplevel()
    booking_window.title("Book a Car")

    tk.Label(booking_window, text="Car ID:").pack(pady=5)
    car_id_entry = tk.Entry(booking_window)
    car_id_entry.pack(pady=5)

    tk.Label(booking_window, text="Customer Name:").pack(pady=5)
    customer_name_entry = tk.Entry(booking_window)
    customer_name_entry.pack(pady=5)

    tk.Label(booking_window, text="Customer Phone:").pack(pady=5)
    customer_phone_entry = tk.Entry(booking_window)
    customer_phone_entry.pack(pady=5)

    tk.Button(booking_window, text="Submit", command=submit_booking).pack(pady=10)


# Function to view rental history
def view_history():
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.rental_id, c.name, c.phone, r.rental_date, r.return_date
        FROM rentals r
        JOIN customers c ON r.customer_id = c.customer_id
    """)
    rentals = cursor.fetchall()
    conn.close()

    if rentals:
        result = "Rental History:\n\n"
        for rental in rentals:
            result += f"Rental ID: {rental[0]}, Customer: {rental[1]} ({rental[2]}), Rental Date: {rental[3]}, Return Date: {rental[4] or 'N/A'}\n"
        messagebox.showinfo("Rental History", result)
    else:
        messagebox.showinfo("Rental History", "No rental history found.")


# Function to add a new car
def add_car():
    def submit_car():
        model = model_entry.get()
        price = price_entry.get()

        if not model or not price:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = sqlite3.connect("car_rental.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cars (model, available, price_per_day) VALUES (?, 1, ?)", (model, price))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Car added successfully!")
        add_car_window.destroy()

    add_car_window = tk.Toplevel()
    add_car_window.title("Add a Car")

    tk.Label(add_car_window, text="Model:").pack(pady=5)
    model_entry = tk.Entry(add_car_window)
    model_entry.pack(pady=5)

    tk.Label(add_car_window, text="Price per Day:").pack(pady=5)
    price_entry = tk.Entry(add_car_window)
    price_entry.pack(pady=5)

    tk.Button(add_car_window, text="Submit", command=submit_car).pack(pady=10)


# Function to update an existing car
def update_car():
    def submit_updates():
        id = id_entry.get()
        model = model_entry.get()
        price = price_entry.get()

        if not model or not price:
            messagebox.showerror("Error", "All fields are required.")
            return
    
        conn = sqlite3.connect("car_rental.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cars WHERE car_id = ?", (id))
        car = cursor.fetchone()
        if not car:
            messagebox.showerror("Error","Invalid Car ID.")

        cursor.execute("UPDATE cars SET model = ?, available = 1, price_per_day = ? WHERE car_id = ?", (model, price, id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Car updated successfully!")
        update_car_window.destroy()

    update_car_window = tk.Toplevel()
    update_car_window.title("Update an Existing Car")

    tk.Label(update_car_window, text="ID of Car to Update:").pack(pady=5)
    id_entry = tk.Entry(update_car_window)
    id_entry.pack(pady=5)

    tk.Label(update_car_window, text="Model:").pack(pady=5)
    model_entry = tk.Entry(update_car_window)
    model_entry.pack(pady=5)

    tk.Label(update_car_window, text="Price per Day:").pack(pady=5)
    price_entry = tk.Entry(update_car_window)
    price_entry.pack(pady=5)

    tk.Button(update_car_window, text="Submit", command=submit_updates).pack(pady=10)


# Function to delete an existing car
def delete_car():
    def submit_deletion():
        id = id_entry.get()

        if not id:
            messagebox.showerror("Error", "Car ID Required.")
            return
        
        conn = sqlite3.connect("car_rental.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE car_id = ?", (id))
        car = cursor.fetchone()

        if not car:
            messagebox.showerror("Error","Invalid Car ID.")
            return
        
        if messagebox.askyesno("Are you sure?", "This action cannot be undone."):
            cursor.execute("DELETE FROM cars WHERE car_id = ?", (id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Car deleted successfully")
            delete_car_window.destroy()
            return
        else:
            return

    delete_car_window = tk.Toplevel()
    delete_car_window.title("Delete an Existing Car")

    tk.Label(delete_car_window, text="ID of Car to Delete:").pack(pady=5)
    id_entry = tk.Entry(delete_car_window)
    id_entry.pack(pady=5)

    tk.Button(delete_car_window, text="Submit", command=submit_deletion).pack(pady=10)

# Function to view all customers
def view_customers():
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    conn.close()

    if customers:
        result = "Customers:\n\n"
        for customer in customers:
            result += f"Customer ID: {customer[0]}, Name: {customer[1]}, Phone: ${customer[2]}\n"
        messagebox.showinfo("View Customers", result)
    else:
        messagebox.showinfo("View Customers", "No customers available.")

# Admin Tab Functionality
def admin_tab_content(frame):
    # Barebones password protection. For the sake of the demonstration, the username is "admin" and the password is just "1234".
    def verify_admin():
        global is_admin

        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "1234":
            is_admin = True
            for widget in frame.winfo_children():
                widget.destroy()
            admin_tab_content(frame)
            messagebox.showinfo("Success", f"Logged in as: {username}")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    tk.Label(frame, text="Admin Panel", font=("Arial", 16)).pack(pady=10)

    if not is_admin:
        tk.Label(frame, text="Username:").pack(pady=5)
        username_entry = tk.Entry(frame)
        username_entry.pack(pady=5)

        tk.Label(frame, text="Password:").pack(pady=5)
        password_entry = tk.Entry(frame)
        password_entry.pack(pady=5)

        tk.Button(frame, text="Login", command=verify_admin).pack(pady=10)
    else:
        # Search Car
        search_btn = tk.Button(frame, text="Search Cars", command=view_cars).pack(pady=5)

        # Add Car
        add_car_btn = tk.Button(frame, text="Add Car", command=add_car).pack(pady=5)

        # Update Car
        update_car_btn = tk.Button(frame, text="Update Car", command=update_car).pack(pady=5)

        # Delete Car
        delete_car_btn = tk.Button(frame, text="Delete Car", command=delete_car).pack(pady=5)

        # View Customers
        view_customers_btn = tk.Button(frame, text="View Customers", command=view_customers).pack(pady=5)

        # Manage Rentals
        rentals_btn = tk.Button(frame, text="View Rental History", command=view_history).pack(pady=5)


# Customer Tab Functionality
def customer_tab_content(frame):
    tk.Label(frame, text="Search Available Cars", font=("Arial", 16)).pack(pady=10)

    search_btn = tk.Button(frame, text="Search Cars", command=view_cars).pack(pady=5)

    # Book Car
    tk.Label(frame, text="Book a Car", font=("Arial", 16)).pack(pady=10)
    book_btn = tk.Button(frame, text="Book Car", command=book_car).pack(pady=5)

    # View History
    tk.Label(frame, text="View Rental History", font=("Arial", 16)).pack(pady=10)
    history_btn = tk.Button(frame, text="View History", command=view_history).pack(pady=5)


# Main Application
def main():
    root = tk.Tk()
    root.title("Car Rental System")
    root.geometry("800x600")

    # Tabs for Admin and Customer
    tab_control = ttk.Notebook(root)

    customer_tab = ttk.Frame(tab_control)
    admin_tab = ttk.Frame(tab_control)

    tab_control.add(customer_tab, text="Customer")
    tab_control.add(admin_tab, text="Admin")

    tab_control.pack(expand=1, fill="both")

    # Customer Tab Content
    customer_tab_content(customer_tab)

    # Admin Tab Content
    admin_tab_content(admin_tab)

    root.mainloop()

if __name__ == "__main__":
    main()