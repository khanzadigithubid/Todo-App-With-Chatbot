from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from src.todo.storage import TodoCRUDSubagent
from src.todo.service import TodoService
import re


def print_menu(console):
    """Print the interactive menu."""
    menu_text = Text()
    menu_text.append("1. Add Task\n", style="bold green")
    menu_text.append("2. List Tasks\n", style="bold blue")
    menu_text.append("3. Update Task\n", style="bold yellow")
    menu_text.append("4. Delete Task\n", style="bold red")
    menu_text.append("5. Complete Task\n", style="bold cyan")
    menu_text.append("6. Mark Incomplete\n", style="bold magenta")
    menu_text.append("7. AI Task Suggestions\n", style="bold green")
    menu_text.append("8. Prioritize Tasks\n", style="bold blue")
    menu_text.append("9. Exit", style="bold white")

    panel = Panel(
        menu_text,
        title="[bold purple]AI-Powered Todo App[/bold purple]",
        subtitle="[italic]Your tasks, organized with AI![/italic]",
        border_style="purple",
        expand=False
    )

    console.print(panel)
    console.print("\n[yellow]Choose an option:[/yellow] ", end="")


def print_header(console, title):
    """Print a formatted header."""
    header = Panel(
        f"[bold]{title}[/bold]",
        border_style="blue",
        expand=False
    )
    console.print(header)
    console.print()  # Empty line for spacing


def get_user_input(console, prompt):
    """Get input from the user with proper styling."""
    console.print(f"[bold]{prompt}[/bold]: ", end="")
    return input().strip()


def add_task_interactive(console, service):
    """Interactive task addition flow."""
    print_header(console, "Add New Task")

    title = get_user_input(console, "Enter task title")
    if not title:
        console.print("[red]Task title cannot be empty![/red]")
        return

    description = get_user_input(console, "Enter task description (optional, press Enter to skip)")
    if not description:
        description = None

    try:
        task = service.add_task(title, description)
        console.print(f"[green]Task created successfully![/green] (ID: {task.id})\n")
    except ValueError as e:
        console.print(f"[red]{str(e)}[/red]\n")


def list_tasks_interactive(console, service):
    """Interactive task listing."""
    print_header(console, "Task List")

    tasks = service.get_all_tasks()

    if not tasks:
        console.print("[yellow]No tasks found[/yellow]\n")
        return

    # Create a rich table
    table = Table(title="Task List", border_style="blue")
    table.add_column("#", style="dim")
    table.add_column("Status", style="bold")
    table.add_column("Title", style="bold")
    table.add_column("Description", style="italic")
    table.add_column("ID", style="dim", width=8)  # Shortened ID for readability

    for idx, task in enumerate(tasks, 1):
        status = "✓ Done" if task.completed else "○ Pending"
        status_style = "green" if task.completed else "red"
        # Shorten the ID for readability in the table
        short_id = task.id[:8] + "..."
        table.add_row(
            str(idx),
            f"[{status_style}]{status}[/{status_style}]",
            task.title,
            task.description or "",
            short_id
        )

    console.print(table)
    console.print()  # Empty line for spacing


def update_task_interactive(console, service):
    """Interactive task update flow."""
    print_header(console, "Update Task")

    tasks = service.get_all_tasks()
    if not tasks:
        console.print("[yellow]No tasks found[/yellow]\n")
        return

    list_tasks_interactive(console, service)

    task_num = get_user_input(console, "Enter task number to update")
    try:
        task_idx = int(task_num) - 1
        if task_idx < 0 or task_idx >= len(tasks):
            console.print("[red]Invalid task number![/red]\n")
            return

        task = tasks[task_idx]
        console.print(f"[blue]Updating task: {task.title}[/blue]\n")

        new_title = get_user_input(console, f"New title (current: '{task.title}', press Enter to keep current)")
        if not new_title:
            new_title = task.title  # Keep current title if Enter is pressed

        new_description = get_user_input(console, f"New description (current: '{task.description or 'None'}', press Enter to keep current)")
        if new_description == "":  # If user just presses Enter, keep current
            new_description = task.description
        elif not new_description:  # If user enters empty string explicitly, set to None
            new_description = None

        updated_task = service.update_task(task.id, title=new_title, description=new_description)
        console.print(f"[green]Task updated successfully![/green]\n")
    except ValueError:
        console.print("[red]Please enter a valid number![/red]\n")
    except Exception as e:
        console.print(f"[red]{str(e)}[/red]\n")


def delete_task_interactive(console, service):
    """Interactive task deletion flow."""
    print_header(console, "Delete Task")

    tasks = service.get_all_tasks()
    if not tasks:
        console.print("[yellow]No tasks found[/yellow]\n")
        return

    list_tasks_interactive(console, service)

    task_num = get_user_input(console, "Enter task number to delete")
    try:
        task_idx = int(task_num) - 1
        if task_idx < 0 or task_idx >= len(tasks):
            console.print("[red]Invalid task number![/red]\n")
            return

        task = tasks[task_idx]
        console.print(f"[blue]Deleting task: {task.title}[/blue]\n")

        result = service.delete_task(task.id)
        if result:
            console.print(f"[green]Task deleted successfully![/green]\n")
        else:
            console.print(f"[red]Task could not be deleted![/red]\n")
    except ValueError:
        console.print("[red]Please enter a valid number![/red]\n")
    except Exception as e:
        console.print(f"[red]{str(e)}[/red]\n")


def toggle_task_status_interactive(console, service, complete=True):
    """Interactive task completion/incompletion flow."""
    action = "Complete" if complete else "Mark Incomplete"
    print_header(console, f"{action} Task")

    tasks = service.get_all_tasks()
    if not tasks:
        console.print("[yellow]No tasks found[/yellow]\n")
        return

    list_tasks_interactive(console, service)

    task_num = get_user_input(console, f"Enter task number to {'complete' if complete else 'mark incomplete'}")
    try:
        task_idx = int(task_num) - 1
        if task_idx < 0 or task_idx >= len(tasks):
            console.print("[red]Invalid task number![/red]\n")
            return

        task = tasks[task_idx]
        console.print(f"[blue]Toggling task: {task.title}[/blue]\n")

        updated_task = service.toggle_task_status(task.id)
        status_text = "marked as complete" if complete else "marked as incomplete"
        console.print(f"[green]Task {status_text}![/green]\n")
    except ValueError:
        console.print("[red]Please enter a valid number![/red]\n")
    except Exception as e:
        console.print(f"[red]{str(e)}[/red]\n")


def get_ai_task_suggestions_interactive(console, service):
    """Interactive function to get AI task suggestions."""
    print_header(console, "AI Task Suggestions")

    console.print("[cyan]Generating task suggestions based on your current tasks...[/cyan]")
    suggestions = service.get_task_suggestions()

    console.print(f"[green]{suggestions}[/green]")
    console.print()


def prioritize_tasks_interactive(console, service):
    """Interactive function to get AI task prioritization."""
    print_header(console, "AI Task Prioritization")

    if not service.get_all_tasks():
        console.print("[yellow]No tasks found to prioritize[/yellow]\n")
        return

    console.print("[cyan]Analyzing your tasks to suggest priority order...[/cyan]")
    prioritized_tasks = service.prioritize_tasks()

    console.print(f"[green]{prioritized_tasks}[/green]")
    console.print()


def main():
    """Main entry point for the application with interactive menu."""
    console = Console()

    # Initialize storage, subagent, and service
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    while True:
        print_menu(console)

        try:
            choice = input().strip()

            if choice == "1":
                add_task_interactive(console, service)
            elif choice == "2":
                list_tasks_interactive(console, service)
            elif choice == "3":
                update_task_interactive(console, service)
            elif choice == "4":
                delete_task_interactive(console, service)
            elif choice == "5":
                toggle_task_status_interactive(console, service, complete=True)
            elif choice == "6":
                toggle_task_status_interactive(console, service, complete=False)
            elif choice == "7":
                get_ai_task_suggestions_interactive(console, service)
            elif choice == "8":
                prioritize_tasks_interactive(console, service)
            elif choice == "9":
                console.print("[bold green]Bye! Keep being productive![/bold green]")
                break
            else:
                console.print(f"[red]Invalid option '{choice}'. Please choose 1-9.[/red]\n")
        except KeyboardInterrupt:
            console.print("\n[bold red]Bye! Keep being productive![/bold red]")
            break
        except Exception as e:
            console.print(f"[red]An error occurred: {str(e)}[/red]\n")


if __name__ == "__main__":
    main()