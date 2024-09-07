# [Task Tracker CLI](https://roadmap.sh/projects/task-tracker).
Task tracker is a project used to track and manage your tasks. In this task, you will build a simple command line interface (CLI) to track what you need to do, what you have done, and what you are currently working on. This project will help you practice your programming skills, including working with the filesystem, handling user inputs, and building a simple CLI application.


## Requirements
The application should run from the command line, accept user actions and inputs as arguments, and store the tasks in a JSON file. The user should be able to:
- Add, Update, and Delete tasks
- Mark a task as in progress or done
- List all tasks
- List all tasks that are done
- List all tasks that are not done
- List all tasks that are in progress


## Usage
### Ensure the script is executable
Open your teminal and enter the command below to enable the script in executable mode:
```bash
chmod u+x task-cli.py
```

### Add Task
To add a new task, use the command below:
```bash
./task-cli.py add "New Task Description"
```

### List Tasks
To list tasks based on their status, specify the parameter such as; "todo", "in progress", or "done" as shown below:
```bash
./task-cli.py list "todo"
```

To list all, simply remove the parameter after the argument
```bash
./task-cli.py list
```

### Update Task Description
To update the description of a task, use the `update` argument with the `task ID` and then provide the `new description` as shown below:
```bash
./task-cli.py update 2 "Updated Task Description"
```

### Mark Task As In Progress
To mark a task as "in progress", use the `mark-in-progress` argument with the `task ID` as parameter as shown below:
```bash
./task_cli.py mark-in-progress 2
```

### Mark Task As Done
To mark a task as "done", use the `mark-done` argument with the `task ID` as parameter as shown below:
```bash
./task_cli.py mark-done 1
```

### Delete Task
To delete a task, use the `delete` argument with the `task ID` as parameter as shown below:
```bash
./task_cli.py delete 2
```


## Notes
- Ensure that the `tasks.json` file exists in the same directory as the script for it to function correctly.
- The application will create the `tasks.json` file if it does not already exist when adding a new task.
