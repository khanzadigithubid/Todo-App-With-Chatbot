# src/todo/interface.py

from .storage import storage
from .models import Task
from typing import Optional

class TodoApp:
    def __init__(self):
        self.running = True

    def display_menu(self):
        print("\n" + "="*50)
        print("TODO APPLICATION - CONSOLE INTERFACE")
        print("="*50)
        print("1. Add Task")
        print("2. List All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task as Complete/Incomplete")
        print("6. Exit")
        print("-"*50)

    def get_user_choice(self):
        try:
            choice = int(input("Enter your choice (1-6): "))
            return choice
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")
            return None

    def add_task(self):
        print("\n--- ADD TASK ---")
        title = input("Enter task title: ").strip()
        if not title:
            print("Task title cannot be empty!")
            return

        description = input("Enter task description (optional): ").strip()
        description = description if description else None

        priority = input("Enter priority (low/medium/high) [default: medium]: ").strip().lower()
        if priority not in ["low", "medium", "high"]:
            priority = "medium"

        task = storage.create_task(title, description, priority)
        print(f"Task '{task.title}' added successfully with ID {task.id}!")

    def list_tasks(self):
        print("\n--- LIST ALL TASKS ---")
        tasks = storage.get_all_tasks()
        
        if not tasks:
            print("No tasks found.")
            return

        print(f"{'ID':<3} {'Title':<20} {'Status':<10} {'Priority':<10} {'Description':<30}")
        print("-" * 80)
        for task in tasks:
            status = "✓ Completed" if task.completed else "○ Pending"
            status_color = "green" if task.completed else "red"
            description = task.description if task.description else ""
            print(f"{task.id:<3} {task.title[:19]:<20} {status:<10} {task.priority.value:<10} {description[:29]:<30}")

    def update_task(self):
        print("\n--- UPDATE TASK ---")
        try:
            task_id = int(input("Enter task ID to update: "))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        task = storage.get_task_by_id(task_id)
        if not task:
            print(f"No task found with ID {task_id}.")
            return

        print(f"Current task: {task.title}")
        new_title = input(f"Enter new title (current: '{task.title}'): ").strip()
        new_title = new_title if new_title else None

        new_description = input(f"Enter new description (current: '{task.description or 'None'}'): ").strip()
        if new_description == "":
            new_description = None  # This means no change

        new_priority = input(f"Enter new priority (low/medium/high) (current: '{task.priority.value}'): ").strip().lower()
        if new_priority not in ["low", "medium", "high", ""]:
            print("Invalid priority. Keeping current priority.")
            new_priority = None
        elif new_priority == "":
            new_priority = None

        updated_task = storage.update_task(task_id, new_title, new_description, None, new_priority)
        if updated_task:
            print(f"Task {task_id} updated successfully!")
        else:
            print("Failed to update task.")

    def delete_task(self):
        print("\n--- DELETE TASK ---")
        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        task = storage.get_task_by_id(task_id)
        if not task:
            print(f"No task found with ID {task_id}.")
            return

        confirm = input(f"Are you sure you want to delete task '{task.title}'? (y/N): ").lower()
        if confirm == 'y':
            success = storage.delete_task(task_id)
            if success:
                print(f"Task {task_id} deleted successfully!")
            else:
                print("Failed to delete task.")
        else:
            print("Deletion cancelled.")

    def toggle_task_completion(self):
        print("\n--- TOGGLE TASK COMPLETION ---")
        try:
            task_id = int(input("Enter task ID to toggle completion: "))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        task = storage.get_task_by_id(task_id)
        if not task:
            print(f"No task found with ID {task_id}.")
            return

        updated_task = storage.toggle_task_completion(task_id)
        if updated_task:
            status = "completed" if updated_task.completed else "incomplete"
            print(f"Task '{updated_task.title}' marked as {status}!")
        else:
            print("Failed to toggle task completion.")

    def run(self):
        print("Welcome to the Todo Application!")
        while self.running:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == 1:
                self.add_task()
            elif choice == 2:
                self.list_tasks()
            elif choice == 3:
                self.update_task()
            elif choice == 4:
                self.delete_task()
            elif choice == 5:
                self.toggle_task_completion()
            elif choice == 6:
                print("Thank you for using the Todo Application. Goodbye!")
                self.running = False
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")