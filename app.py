import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Create main application window
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

# Customer Tab Functionality
def customer_tab_content(frame):
    tk.Label(frame, text="Search Available Cars", font=("Arial", 16)).pack(pady=10)
    
    search_btn = tk.Button(frame, text="Search Cars", command=search_cars)
    search_btn.pack(pady=5)

    # Book Car
    tk.Label(frame, text="Book a Car", font=("Arial", 16)).pack(pady=10)
    book_btn = tk.Button(frame, text="Book Car", command=book_car)
    book_btn.pack(pady=5)

    # View History
    tk.Label(frame, text="View Rental History", font=("Arial", 16)).pack(pady=10)
    history_btn = tk.Button(frame, text="View History", command=view_history)
    history_btn.pack(pady=5)

# Admin Tab Functionality
def admin_tab_content(frame):
    tk.Label(frame, text="Admin Panel", font=("Arial", 16)).pack(pady=10)

    # Add Car
    add_car_btn = tk.Button(frame, text="Add Car", command=add_car)
    add_car_btn.pack(pady=5)

    # Manage Rentals
    rentals_btn = tk.Button(frame, text="Manage Rentals", command=manage_rentals)
    rentals_btn.pack(pady=5)

    # Maintenance
    maintenance_btn = tk.Button(frame, text="Manage Maintenance", command=manage_maintenance)
    maintenance_btn.pack(pady=5)

# Placeholder Functions
def search_cars():
    messagebox.showinfo("Search Cars", "Feature not implemented yet.")

def book_car():
    messagebox.showinfo("Book Car", "Feature not implemented yet.")

def view_history():
    messagebox.showinfo("View History", "Feature not implemented yet.")

def add_car():
    messagebox.showinfo("Add Car", "Feature not implemented yet.")

def manage_rentals():
    messagebox.showinfo("Manage Rentals", "Feature not implemented yet.")

def manage_maintenance():
    messagebox.showinfo("Manage Maintenance", "Feature not implemented yet.")

# Run the application
if __name__ == "__main__":
    main()
