
# Personal Expense Tracker

## Overview
The Personal Expense Tracker is a user-friendly application designed to help individuals track their daily expenses, categorize them, and visualize spending habits. It is ideal for those who want to manage their finances more effectively by keeping a record of where their money goes.

## Features
- **Add Expenses**: Easily log your expenses with details such as date, category, amount, and description.
- **Categorize Expenses**: Organize your expenses by categories such as Food, Transport, Entertainment, Bills, and Other.
- **Delete Expenses**: Remove specific expenses or delete all expenses at once.
- **View Expense Summary**: Get a summary of your total expenses in GBP, converted from various currencies.
- **Visualize Spending**: Use built-in tools to plot and visualize your spending trends by category.
- **Clear Input Form**: Reset the input form to its default state after adding an expense.
- **Stylish Interface**: A clean and modern interface for a pleasant user experience.
- **Responsive Layout**: The application window centers itself on the screen for better accessibility.

## Technologies Used
- **Programming Language**: Python
- **Libraries**:
  - **pandas**: For data manipulation and handling CSV files.
  - **Matplotlib**: For creating visualizations of spending trends.
  - **tkinter**: For building the graphical user interface.
  - **tkcalendar**: For selecting dates easily within the GUI.
  - **ttk**: For enhanced widget styling in the interface.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mcneillium/expense-tracker.git
   cd expense-tracker
   ```

2. **Create a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scriptsctivate`
   ```

3. **Install Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python main_gui.py
   ```

## Usage
1. **Adding Expenses**: Enter the date, category, amount, currency, and a brief description of the expense, then click "Add Expense".
2. **Viewing Expenses**: All added expenses are displayed in a table view with details. You can see the total expenses in GBP at the bottom.
3. **Deleting Expenses**: Select an expense from the table and click "Delete Expense" to remove it. Click "Delete All Expenses" to clear the entire list.
4. **Visualizing Spending**: Click "Plot Expenses" to generate a bar chart showing your spending by category.
5. **Clearing the Form**: Click "Clear Form" to reset the input fields.

## Contribution
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions or find any bugs.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For any inquiries or feedback, please contact paulmcneill1989@hotmail.co.uk.
