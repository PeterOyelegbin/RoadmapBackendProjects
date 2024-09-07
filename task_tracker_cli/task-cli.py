#!/usr/bin/env python3

import json
import os
import argparse
from datetime import datetime

# Path to the JSON file where tasks are stored
FILE_PATH = 'tasks.json'

# Format time to dd-mm-yy HH:MM
current_date = datetime.now()
formatted_date = current_date.strftime('%d %B %Y %H:%M')

# Ensure the JSON file exists
if not os.path.isfile(FILE_PATH):
    with open(FILE_PATH, 'w') as file:
        json.dump({}, file, indent=4)

def load_tasks():
    """Load tasks from the JSON file."""
    with open(FILE_PATH, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(FILE_PATH, 'w') as file:
        json.dump(tasks, file, indent=4)

# Add a new task.
def add_task(description):
    tasks = load_tasks()
    task_id = str(max([int(k) for k in tasks.keys()] + [0]) + 1)
    tasks[task_id] = {"description": description, "status": "todo", "createdAt": formatted_date, "updatedAt": "N/A"}
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

# Update an existing task.
def update_task(task_id, description):
    tasks = load_tasks()
    if task_id in tasks:
        tasks[task_id]["description"] = description
        tasks[task_id]["updatedAt"] = formatted_date
        save_tasks(tasks)
        print(f"Task {task_id} updated successfully")
    else:
        print(f"Task {task_id} not found")

# Delete a task.
def delete_task(task_id):
    tasks = load_tasks()
    if task_id in tasks:
        del tasks[task_id]
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully")
    else:
        print(f"Task {task_id} not found")

# Mark a task as in progress.
def mark_in_progress(task_id):
    tasks = load_tasks()
    if task_id in tasks:
        tasks[task_id]["status"] = "in progress"
        tasks[task_id]["updatedAt"] = formatted_date
        save_tasks(tasks)
        print(f"Task {task_id} marked as in progress")
    else:
        print(f"Task {task_id} not found")

# Mark a task as done.
def mark_done(task_id):
    tasks = load_tasks()
    if task_id in tasks:
        tasks[task_id]["status"] = "done"
        tasks[task_id]["updatedAt"] = formatted_date
        save_tasks(tasks)
        print(f"Task {task_id} marked as done")
    else:
        print(f"Task {task_id} not found")

# List tasks based on their status.
def list_tasks(status=None):
    tasks = load_tasks()
    filtered_tasks = {k: v for k, v in tasks.items() if status is None or v["status"] == status}
    if filtered_tasks:
        for task_id, task in filtered_tasks.items():
            print(f"ID: {task_id}, Description: {task['description']}, Status: {task['status']}, CreatedAt: {task['createdAt']}, UpdatedAt: {task['updatedAt']}")
    else:
        print(f"No tasks found for status '{status}'" if status else "No tasks found")


def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for 'add' command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Description of the task')

    # Subparser for 'update' command
    update_parser = subparsers.add_parser('update', help='Update an existing task')
    update_parser.add_argument('task_id', help='ID of the task')
    update_parser.add_argument('description', help='New description of the task')

    # Subparser for 'delete' command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', help='ID of the task')

    # Subparser for 'mark-in-progress' command
    mark_in_progress_parser = subparsers.add_parser('mark-in-progress', help='Mark a task as in progress')
    mark_in_progress_parser.add_argument('task_id', help='ID of the task')
    
    # Subparser for 'mark-done' command
    mark_done_parser = subparsers.add_parser('mark-done', help='Mark a task as done')
    mark_done_parser.add_argument('task_id', help='ID of the task')

    # Subparser for 'list' command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('status', nargs='?', choices=['todo', 'in progress', 'done'], help='Status of the tasks to list')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description)

    elif args.command == 'update':
        update_task(args.task_id, args.description)

    elif args.command == 'delete':
        delete_task(args.task_id)

    elif args.command == 'mark-in-progress':
        mark_in_progress(args.task_id)

    elif args.command == 'mark-done':
        mark_done(args.task_id)

    elif args.command == 'list':
        list_tasks(args.status)

if __name__ == '__main__':
    main()
