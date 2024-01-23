import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, messagebox
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk

class CustomStyle:
    @staticmethod
    def set_custom_style():
        style = ttk.Style()

        style.configure("TNotebook", tabposition="n", background="white", borderwidth=0)
        style.configure("TNotebook.Tab", background="white", foreground="black", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "white")])

        style.configure("TFrame", background="white")

        style.configure("TLabel", background="white", foreground="black")

        style.configure("TButton", background="white", foreground="black", padding=[10, 5])

class Product:
    def __init__(self, id, name, description="", quantity=0, selling_price=0, buying_price=0, expiry_date=None,
                 image_path=None):
        self.id = id
        self.name = name
        self.description = description
        self.quantity = quantity
        self.selling_price = selling_price
        self.buying_price = buying_price
        self.expiry_date = expiry_date
        self.image_path = image_path

# Billing tab class 
class BillingTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        # Bill History Section
        self.bill_history_treeview = ttk.Treeview(self, columns=("Bill No", "Date"))
        self.bill_history_treeview.heading("#0", text="Bill History")
        self.bill_history_treeview.heading("Bill No", text="Bill No")
        self.bill_history_treeview.heading("Date", text="Date")
        self.bill_history_treeview.pack(side="left", fill="both", expand=True)

        # Generate Bill Section
        self.generate_bill_frame = ttk.Frame(self)
        self.generate_bill_frame.pack(side="left", fill="both", expand=True)

        # Search Bar
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.generate_bill_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, padx=10, pady=10)
        search_entry.bind("<Return>", self.add_item_from_search)

        # Search Suggestions Treeview
        self.suggestions_treeview = ttk.Treeview(self.generate_bill_frame, columns=("ID", "Name", "Quantity", "Price"))
        self.suggestions_treeview.heading("#0", text="Suggestions")
        self.suggestions_treeview.heading("ID", text="ID")
        self.suggestions_treeview.heading("Name", text="Name")
        self.suggestions_treeview.heading("Quantity", text="Quantity")
        self.suggestions_treeview.heading("Price", text="Price")
        self.suggestions_treeview.grid(row=1, column=0, padx=10, pady=10)
        self.suggestions_treeview.bind("<Double-Button-1>", self.add_item_from_suggestions)

        # Bill Items Treeview
        self.bill_items_treeview = ttk.Treeview(self.generate_bill_frame, columns=("ID", "Name", "Quantity", "Price"))
        self.bill_items_treeview.heading("#0", text="Bill Items")
        self.bill_items_treeview.heading("ID", text="ID")
        self.bill_items_treeview.heading("Name", text="Name")
        self.bill_items_treeview.heading("Quantity", text="Quantity")
        self.bill_items_treeview.heading("Price", text="Price")
        self.bill_items_treeview.grid(row=1, column=1, padx=10, pady=10)

        # Generate Bill Button
        generate_bill_button = tk.Button(self.generate_bill_frame, text="Generate Bill", command=self.generate_bill)
        generate_bill_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def add_item_from_search(self, event):
        # Placeholder: Implement item addition based on search
        # You can fetch item details from the database based on the search term
        # and add it to the billing items treeview
        pass

    def add_item_from_suggestions(self, event):
        # Placeholder: Implement item addition based on double-click on suggestions
        # You can fetch item details from the selected suggestion and add it to the billing items treeview
        pass

    def generate_bill(self):
        # Placeholder: Implement bill generation logic
        # Calculate total amount, update quantity in the inventory, and save the bill
        pass

class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management App")
        self.geometry("1200x800")
        self.create_widgets()

    def create_widgets(self):
        CustomStyle.set_custom_style()

        # Create Tab Control
        tab_control = ttk.Notebook(self)

        # Add tabs
        inventory_tab = InventoryTab(tab_control)
        products_tab = ProductsTab(tab_control)
        billing_tab = BillingTab(tab_control)

        tab_control.add(inventory_tab, text="Inventory")
        tab_control.add(products_tab, text="Products")
        tab_control.add(billing_tab, text="Billing")

        tab_control.pack(expand=1, fill="both")

class InventoryTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.load_items()

    def create_widgets(self):
        # Create refresh button for inventory
        refresh_button = tk.Button(self, text="Refresh", command=self.load_items)
        refresh_button.pack(side="top", padx=10, pady=10)

        # Create ttk.Treeview for displaying inventory items
        self.inventory_treeview = ttk.Treeview(self, columns=("ID", "Name", "Quantity"))
        self.inventory_treeview.heading("#0", text="Inventory ID")
        self.inventory_treeview.heading("Name", text="Name")
        self.inventory_treeview.heading("Quantity", text="Quantity")
        self.inventory_treeview.pack(fill="both", expand=True)

    def load_items(self):
        # Connect to the database and load item list using SQLite
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                quantity INTEGER,
                selling_price REAL,
                buying_price REAL,
                expiry_date TEXT,
                image_path TEXT
            )
        ''')

        conn.commit()

        # Fetch items from the database
        cursor.execute("SELECT * FROM items")
        item_list = cursor.fetchall()

        conn.close()

        # Placeholder: Update the GUI with loaded items
        self.update_inventory_treeview(item_list)

    def update_inventory_treeview(self, item_list):
        # Clear existing items in the treeview
        for item in self.inventory_treeview.get_children():
            self.inventory_treeview.delete(item)

        # Add loaded items to the treeview
        for product in item_list:
            self.inventory_treeview.insert("", "end", values=product)

class ProductsTab(tk.Frame):
    def __init__(self, master=None, inventory_tab=None):
        super().__init__(master)
        self.inventory_tab = inventory_tab
        self.create_widgets()

    def create_widgets(self):
        add_button = tk.Button(self, text="Add Product", command=self.show_dialog)
        add_button.pack(side="top", padx=10, pady=10)

        # Create ttk.Treeview for displaying products
        self.product_treeview = ttk.Treeview(self, columns=("ID", "Name", "Quantity", "Selling Price"))
        self.product_treeview.heading("#0", text="Product ID")
        self.product_treeview.heading("Name", text="Name")
        self.product_treeview.heading("Quantity", text="Quantity")
        self.product_treeview.heading("Selling Price", text="Selling Price")
        self.product_treeview.pack(fill="both", expand=True)

        # Placeholder: Load and display initial products
        self.load_and_display_products()

    def show_dialog(self):
        # Show dialog to enter attribute values for new product
        dialog = ProductDialog(self)
        self.wait_window(dialog)

        # Access the values entered in the dialog and create a product
        values = dialog.get_values()
        if values:
            new_product = Product(**values)
            self.save_product(new_product)
            # Placeholder: Update the GUI instantly with the new product
            print("New product saved:", new_product.__dict__)
            if self.inventory_tab:
                self.inventory_tab.load_items()

    def save_product(self, product):
        # Connect to the database and save the new product using SQLite
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                quantity INTEGER,
                selling_price REAL,
                buying_price REAL,
                expiry_date TEXT,
                image_path TEXT
            )
        ''')

        # Insert the new product
        cursor.execute('''
            INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (product.id, product.name, product.description, product.quantity,
              product.selling_price, product.buying_price, product.expiry_date, product.image_path))

        conn.commit()
        conn.close()

        # Update the product treeview with the new product
        self.update_product_treeview()

        # Update the inventory treeview as well
        if hasattr(self.master, 'inventory_tab'):
            self.master.inventory_tab.load_items()

    def update_product_treeview(self):
        # Clear existing items in the treeview
        for item in self.product_treeview.get_children():
            self.product_treeview.delete(item)

        # Fetch items from the database
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        item_list = cursor.fetchall()
        conn.close()

        # Add loaded items to the treeview
        for product in item_list:
            self.product_treeview.insert("", "end", values=product)

    def load_and_display_products(self):
        # Fetch items from the database
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        item_list = cursor.fetchall()
        conn.close()

        # Add loaded items to the treeview
        for product in item_list:
            self.product_treeview.insert("", "end", values=product)

class ProductDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Product")
        self.attributes('-topmost', True)  # Make the dialog always on top
        self.create_widgets()

    def create_widgets(self):
        # Create input fields for product attributes
        self.id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.selling_price_var = tk.StringVar()
        self.buying_price_var = tk.StringVar()
        self.expiry_date_var = tk.StringVar()

        tk.Label(self, text="ID:").grid(row=0, column=0, sticky="w")
        tk.Entry(self, textvariable=self.id_var).grid(row=0, column=1)

        tk.Label(self, text="Name:").grid(row=1, column=0, sticky="w")
        tk.Entry(self, textvariable=self.name_var).grid(row=1, column=1)

        tk.Label(self, text="Description:").grid(row=2, column=0, sticky="w")
        tk.Entry(self, textvariable=self.description_var).grid(row=2, column=1)

        tk.Label(self, text="Quantity:").grid(row=3, column=0, sticky="w")
        tk.Entry(self, textvariable=self.quantity_var).grid(row=3, column=1)

        tk.Label(self, text="Selling Price:").grid(row=4, column=0, sticky="w")
        tk.Entry(self, textvariable=self.selling_price_var).grid(row=4, column=1)

        tk.Label(self, text="Buying Price:").grid(row=5, column=0, sticky="w")
        tk.Entry(self, textvariable=self.buying_price_var).grid(row=5, column=1)

        tk.Label(self, text="Expiry Date:").grid(row=6, column=0, sticky="w")
        tk.Entry(self, textvariable=self.expiry_date_var).grid(row=6, column=1)

        # Button to confirm and close the dialog
        tk.Button(self, text="Create Product", command=self.create_product).grid(row=7, column=0, columnspan=2)

    def create_product(self):
        # Get values entered in the dialog
        try:
            values = {
                "id": self.id_var.get(),
                "name": self.name_var.get(),
                "description": self.description_var.get(),
                "quantity": int(self.quantity_var.get()),
                "selling_price": float(self.selling_price_var.get()),
                "buying_price": float(self.buying_price_var.get()),
                "expiry_date": self.expiry_date_var.get(),
            }
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return

        # Close the dialog and save the product
        self.destroy()
        self.master.save_product(Product(**values))  # Save the product

    def get_values(self):
        # Placeholder: Return the values entered in the dialog
        return {
            "id": self.id_var.get(),
            "name": self.name_var.get(),
            "description": self.description_var.get(),
            "quantity": int(self.quantity_var.get()),
            "selling_price": float(self.selling_price_var.get()),
            "buying_price": float(self.buying_price_var.get()),
            "expiry_date": self.expiry_date_var.get(),
        }



if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
