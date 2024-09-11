# [Expense Tracker](https://roadmap.sh/projects/expense-tracker).
Build a simple expense tracker application to manage your finances. The application should allow users to add, delete, and view their expenses. The application should also provide a summary of the expenses.


## Requirements
Application should run from the command line and should have the following features:
- Users can add an expense with a description and amount.
- Users can update an expense.
- Users can delete an expense.
- Users can view all expenses.
- Users can view a summary of all expenses.
- Users can view a summary of expenses for a specific month (of current year).

Here are some additional features that you can add to the application:
- Add expense categories and allow users to filter expenses by category.
- Allow users to set a budget for each month and show a warning when the user exceeds the budget.
- Allow users to export expenses to a CSV file.


## Usage
### Ensure the script is executable
Open your teminal and enter the command below to enable the script in executable mode:
```bash
chmod u+x expense-tracker.py
```

### Add Expense
To add new expense, use the command below:
```bash
./expense-tracker.py add --description "Lunch" --amount 20
```

### List Expense
To list all expense, use the command below:
```bash
./expense-tracker.py list
```

### Update Expense
To update description and amount of an existing expense, use the command below:
```bash
./expense-tracker.py update --id 1 --description "Dinner" --amount 15
```

For a specific field either description or amount, use the `update` argument with `--id` `<expense-id>` and `--description` or `--amount` and `<value>` as shown below:
```bash
./expense-tracker.py update --id 1 --amount 30
```

### Expense Summary
To get the summary of the expense for a particular month, use the `summary` argument with `--month` and `<month-in-digit>` as shown below:
```bash
./expense-tracker.py summary --month 9
```

For summary of all record, use the command below:
```bash
./expense-tracker.py summary
```

### Delete Expense
To delete an expense, use the `delete` argument with `--id` and `<expense ID>` as shown below:
```bash
./expense-tracker.py delete --id 1
```


## Notes
- Ensure that the `expenses.csv` file exists in the same directory as the script for it to function correctly.
- The application will create the `expenses.csv` file if it does not already exist when adding a new task.
