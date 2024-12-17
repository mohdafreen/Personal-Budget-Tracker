import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Database functions
def add_transaction(date, category, description, amount):
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (date, category, description, amount) VALUES (?, ?, ?, ?)",
                   (date, category, description, amount))
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    return rows

# GUI functions
def add_transaction_gui():
    date = entry_date.get()
    category = entry_category.get()
    description = entry_description.get()
    amount = entry_amount.get()
    
    if date and category and description and amount:
        try:
            amount = float(amount)
            add_transaction(date, category, description, amount)
            messagebox.showinfo("Success", "Transaction added successfully!")
            entry_date.delete(0, END)
            entry_category.delete(0, END)
            entry_description.delete(0, END)
            entry_amount.delete(0, END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
    else:
        messagebox.showerror("Error", "All fields are required.")

def show_transactions_gui():
    transactions = get_transactions()
    transactions_window = Toplevel()
    transactions_window.title("Transactions")
    
    for index, transaction in enumerate(transactions):
        for col_index, value in enumerate(transaction):
            Label(transactions_window, text=value).grid(row=index, column=col_index)

def plot_expenses_gui():
    transactions = get_transactions()
    df = pd.DataFrame(transactions, columns=['ID', 'Date', 'Category', 'Description', 'Amount'])
    
    expenses = df[df['Amount'] < 0].groupby('Category')['Amount'].sum()
    
    if not expenses.empty:
        expenses.plot(kind='bar')
        plt.title("Expenses by Category")
        plt.ylabel("Amount")
        plt.show()
    else:
        messagebox.showinfo("Info", "No expenses to plot.")

# Main GUI
root = Tk()
root.title("Personal Budget Tracker")

Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
entry_date = Entry(root)
entry_date.grid(row=0, column=1)

Label(root, text="Category:").grid(row=1, column=0)
entry_category = Entry(root)
entry_category.grid(row=1, column=1)

Label(root, text="Description:").grid(row=2, column=0)
entry_description = Entry(root)
entry_description.grid(row=2, column=1)

Label(root, text="Amount:").grid(row=3, column=0)
entry_amount = Entry(root)
entry_amount.grid(row=3, column=1)

Button(root, text="Add Transaction", command=add_transaction_gui).grid(row=4, column=0, columnspan=2)
Button(root, text="Show Transactions", command=show_transactions_gui).grid(row=5, column=0, columnspan=2)
Button(root, text="Plot Expenses", command=plot_expenses_gui).grid(row=6, column=0, columnspan=2)

root.mainloop()
