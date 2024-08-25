import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# CSV file path
csv_file = 'expenses.csv'

# Currency conversion rates
conversion_rates = {
    "£": 1.00,
    "$": 0.75,  # Example rate, 1 USD = 0.75 GBP
    "€": 0.85,  # Example rate, 1 EUR = 0.85 GBP
    "¥": 0.0055  # Example rate, 1 JPY = 0.0055 GBP
}

# Initialize the CSV file with the necessary columns if it doesn't exist
def initialize_csv():
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
        df.to_csv(csv_file, index=False)
    else:
        df = pd.read_csv(csv_file)
        if set(['Date', 'Category', 'Amount', 'Description']).issubset(df.columns) == False:
            df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
            df.to_csv(csv_file, index=False)

# Add a new expense to the CSV file and update the display
def add_expense():
    date = date_entry.get_date().strftime("%Y-%m-%d")  # Get the date in the correct format
    category = category_var.get().strip()
    amount = amount_entry.get().strip()
    description = description_entry.get().strip()
    currency = currency_var.get().strip()

    if date and category and amount and description:
        try:
            amount = float(amount)
            df = pd.DataFrame([[date, category, f"{currency}{amount:.2f}", description]],
                              columns=['Date', 'Category', 'Amount', 'Description'])
            df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)
            load_expenses()
            clear_inputs()
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for the amount.")
    else:
        messagebox.showwarning("Input Error", "Please fill out all fields correctly.")

# Load expenses from the CSV file into the Treeview
def load_expenses():
    for item in expenses_list.get_children():
        expenses_list.delete(item)

    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            expenses_list.insert('', tk.END, values=row.tolist())

    update_summary()

# Update the summary label with the total expenses in GBP
def update_summary():
    total_gbp = 0
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            currency_symbol = row['Amount'][0]
            if currency_symbol in conversion_rates:
                amount = float(row['Amount'][1:])
                amount_in_gbp = amount * conversion_rates[currency_symbol]
                total_gbp += amount_in_gbp
            else:
                messagebox.showwarning("Currency Error", f"Unrecognized currency symbol in entry: {row['Amount']}")
                continue

    summary_label.config(text=f"Total Expenses: £{total_gbp:.2f}")

# Plot expenses by category using a bar chart
def plot_expenses_gui():
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        if df.empty:
            messagebox.showinfo("No Data", "No expenses to plot.")
            return
        category_totals = df.groupby('Category')['Amount'].apply(lambda x: x.str[1:].astype(float).sum())
        category_totals.plot(kind='bar')
        plt.title('Total Spending by Category')
        plt.xlabel('Category')
        plt.ylabel('Total Amount (£)')
        plt.show()
    else:
        messagebox.showinfo("No Data", "No expenses to plot.")

# Delete the selected expense from the CSV file and update the display
def delete_expense():
    selected_item = expenses_list.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an expense to delete.")
        return

    # Get selected item details
    item = expenses_list.item(selected_item)
    values = item['values']

    # Load existing data
    df = pd.read_csv(csv_file)

    # Remove the selected row
    df = df[~((df['Date'] == values[0]) & (df['Category'] == values[1]) & 
              (df['Amount'] == values[2]) & (df['Description'] == values[3]))]

    # Save the updated DataFrame back to the CSV
    df.to_csv(csv_file, index=False)

    # Refresh the Treeview
    load_expenses()

    messagebox.showinfo("Success", "Expense deleted successfully!")

# Delete all expenses from the CSV file and update the display
def delete_all_expenses():
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all expenses?"):
        # Clear the CSV file
        initialize_csv()
        # Refresh the Treeview
        load_expenses()
        messagebox.showinfo("Success", "All expenses have been deleted.")

# Clear all input fields to their default states
def clear_inputs():
    date_entry.set_date(datetime.now())
    category_var.set("")
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    currency_var.set("£")

# Center the main window on the screen
def center_window(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Set up the main window
root = tk.Tk()
root.title("Expense Tracker by Paul Martin McNeill")
root.geometry("800x650")
root.resizable(False, False)

# Center the window
center_window(root)

# Set a style for the widgets
style = ttk.Style(root)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12), padding=6)
style.configure("TCombobox", font=("Helvetica", 12))
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

# Title
title_label = tk.Label(root, text="Expense Tracker", font=("Helvetica", 20, "bold"))
title_label.grid(row=0, column=0, columnspan=5, padx=10, pady=20)

# Date field
tk.Label(root, text="Date:").grid(row=1, column=0, padx=10, pady=10)
date_entry = DateEntry(root, date_pattern="dd/mm/yyyy")
date_entry.set_date(datetime.now())
date_entry.grid(row=1, column=1, padx=10, pady=10)

# Category field
tk.Label(root, text="Category:").grid(row=2, column=0, padx=10, pady=10)
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var, values=["Food", "Transport", "Entertainment", "Bills", "Other"], state="readonly")
category_dropdown.grid(row=2, column=1, padx=10, pady=10)

# Amount field
tk.Label(root, text="Amount:").grid(row=3, column=0, padx=10, pady=10)
amount_entry = tk.Entry(root)
amount_entry.grid(row=3, column=1, padx=10, pady=10)

# Currency dropdown
tk.Label(root, text="Currency:").grid(row=4, column=0, padx=10, pady=10)
currency_var = tk.StringVar(value="£")
currency_dropdown = ttk.Combobox(root, textvariable=currency_var, values=["£", "$", "€", "¥"], state="readonly")
currency_dropdown.grid(row=4, column=1, padx=10, pady=10)

# Description field
tk.Label(root, text="Description:").grid(row=5, column=0, padx=10, pady=10)
description_entry = tk.Entry(root)
description_entry.grid(row=5, column=1, padx=10, pady=10)

# Add, Plot, Clear, Delete, and Delete All Buttons
add_button = ttk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=6, column=0, padx=10, pady=10)
plot_button = ttk.Button(root, text="Plot Expenses", command=plot_expenses_gui)
plot_button.grid(row=6, column=1, padx=10, pady=10)
clear_button = ttk.Button(root, text="Clear Form", command=clear_inputs)
clear_button.grid(row=1, column=2, padx=10, pady=10)
delete_button = ttk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.grid(row=6, column=2, padx=10, pady=10)
delete_all_button = ttk.Button(root, text="Delete All Expenses", command=delete_all_expenses)
delete_all_button.grid(row=6, column=3, padx=10, pady=10)

# Expense list (Treeview)
columns = ("Date", "Category", "Amount", "Description")
expenses_list = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    expenses_list.heading(col, text=col)
expenses_list.grid(row=7, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

# Summary
summary_label = tk.Label(root, text="Total Expenses: £0.00", font=("Helvetica", 14, "bold"))
summary_label.grid(row=8, column=0, columnspan=5, padx=10, pady=20)

# Initialize the CSV file and load the expenses
initialize_csv()
load_expenses()

# Start the main loop
root.mainloop()
