#!/usr/bin/env python3

import csv, os, argparse
from datetime import datetime


# Path to the JSON file where tasks are stored
DATA_FILE = './expense_tracker/expenses.csv'

# Format time to dd-mm-yy HH:MM
current_date = datetime.now().strftime('%Y-%m-%d')

def load_data():
    expenses = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append({
                    'id': int(row['id']),
                    'date': row['date'],
                    'description': row['description'],
                    'amount': float(row['amount']),
                    'update_At': row['update_At']
                })
    return expenses

def save_data(expenses):
    with open(DATA_FILE, 'w', newline='') as file:
        fieldnames = ['id', 'date', 'description', 'amount', 'update_At']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for exp in expenses:
            writer.writerow(exp)

# Add a new expense.
def add_expense(description, amount):
    expenses = load_data()
    expense_id = max([exp['id'] for exp in expenses], default=0) + 1
    expense = {
        'id': expense_id,
        'date': current_date,
        'description': description,
        'amount': amount,
        'update_At': "N/A"

    }
    expenses.append(expense)
    save_data(expenses)
    print(f'Expense added successfully (ID: {expense_id})')

# Update an existing expense.
def update_expense(expense_id, description=None, amount=None):
    expenses = load_data()
    expense_found = False
    for exp in expenses:
        if exp['id'] == expense_id:
            exp['update_At'] = current_date
            if description is not None:
                exp['description'] = description
            if amount is not None:
                exp['amount'] = amount
            expense_found = True
            break
    if expense_found:
        save_data(expenses)
        print(f'Expense ID {expense_id} updated successfully')
    else:
        print(f'Expense with ID {expense_id} not found')

# Delete an expense
def delete_expense(expense_id):
    expenses = load_data()
    expense_found = False
    for exp in expenses:
        if exp['id'] == expense_id:
            expense_found = True
            break
    if expense_found:
        expenses = [exp for exp in expenses if exp['id'] != expense_id]
        save_data(expenses)
        print(f'Expense ID {expense_id} deleted successfully')
    else:
        print(f'Expense with ID {expense_id} not found')

# List all expense
def list_expenses():
    expenses = load_data()
    print(f"{'ID':<5} {'Date':<12} {'Description':<15} {'Amount':<7} {'UpdatedAt':<12}")
    for exp in expenses:
        print(f"{exp['id']:<5} {exp['date']:<12} {exp['description']:<15} ${exp['amount']:<7} {exp['update_At']:<12}")

# Summary of expense
def summary(month=None):
    expenses = load_data()
    total = 0
    for exp in expenses:
        if month:
            exp_month = datetime.strptime(exp['date'], '%Y-%m-%d').month
            if exp_month != month:
                continue
        total += exp['amount']
    if month:
        print(f'Total expenses for month {month}: ${total}')
    else:
        print(f'Total expenses: ${total}')


def main():
    parser = argparse.ArgumentParser(description='Expense Tracker CLI')
    subparsers = parser.add_subparsers(dest='command')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('--description', required=True, help='Description of the expense')
    add_parser.add_argument('--amount', type=float, required=True, help='Amount of the expense')

    # update command
    update_parser = subparsers.add_parser('update', help='Update an existing expense')
    update_parser.add_argument('--id', type=int, required=True, help='ID of the expense to update')
    update_parser.add_argument('--description', help='New description of the expense')
    update_parser.add_argument('--amount', type=float, help='New amount of the expense')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('--id', type=int, required=True, help='ID of the expense to delete')

    # List command
    subparsers.add_parser('list', help='List all expenses')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show the summary of expenses')
    summary_parser.add_argument('--month', type=int, help='Month to filter expenses by (1-12)')

    args = parser.parse_args()

    if args.command == 'add':
        add_expense(args.description, args.amount)
    elif args.command == 'update':
        update_expense(args.id, args.description, args.amount)
    elif args.command == 'delete':
        delete_expense(args.id)
    elif args.command == 'list':
        list_expenses()
    elif args.command == 'summary':
        summary(args.month)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
