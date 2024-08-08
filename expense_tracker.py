import pandas as pd
import matplotlib.pyplot as plt

def add_expense(date, category, amount, description):
    expense = {'Date': date, 'Category': category, 'Amount': amount, 'Description': description}
    df = pd.DataFrame([expense])
    df.to_csv('expenses.csv', mode='a', header=False, index=False)

def get_expenses():
    return pd.read_csv('expenses.csv')

def plot_expenses():
    df = pd.read_csv('expenses.csv')
    category_totals = df.groupby('Category')['Amount'].sum()
    category_totals.plot(kind='bar')
    plt.title('Total Spending by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.show()

# Example usage
if __name__ == "__main__":
    add_expense('2023-11-01', 'Food', 10.5, 'Lunch')
    add_expense('2023-11-01', 'Transport', 5.0, 'Bus fare')
    plot_expenses()
