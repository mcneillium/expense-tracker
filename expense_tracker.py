import pandas as pd
import os
import matplotlib.pyplot as plt

# Path to the CSV file
csv_file = 'expenses.csv'

def initialize_csv():
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
        df.to_csv(csv_file, index=False)
    else:
        df = pd.read_csv(csv_file)
        if set(['Date', 'Category', 'Amount', 'Description']).issubset(df.columns) == False:
            df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
            df.to_csv(csv_file, index=False)

def add_expense(date, category, amount, description):
    expense = {'Date': date, 'Category': category, 'Amount': amount, 'Description': description}
    df = pd.DataFrame([expense])
    if not os.path.exists(csv_file):
        initialize_csv()
    df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)

def get_expenses():
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def plot_expenses():
    df = get_expenses()
    if df.empty:
        print("No expenses to plot.")
        return
    if 'Category' not in df.columns or 'Amount' not in df.columns:
        print("The required columns are not present in the CSV file.")
        return
    category_totals = df.groupby('Category')['Amount'].sum()
    category_totals.plot(kind='bar')
    plt.title('Total Spending by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.show()

# Initialize CSV with headers if it doesn't exist
initialize_csv()

# Example usage
if __name__ == "__main__":
    add_expense('2023-11-01', 'Food', 10.5, 'Lunch')
    add_expense('2023-11-01', 'Transport', 5.0, 'Bus fare')
    plot_expenses()
