import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .models import Task
from .service import TodoService
from .storage import TodoCRUDSubagent

# Initialize the Typer app
app = typer.Typer()

# Initialize console for rich output
console = Console()

# Initialize storage, subagent, and service
subagent = TodoCRUDSubagent()
service = TodoService(subagent)


@app.command()
def add(
    title: str = typer.Argument(..., help="Title of the task"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Description of the task")
):
    """
    Add a new task with title and optional description.
    """
    try:
        # Validate title length (1-200 chars)
        if len(title) < 1 or len(title) > 200:
            console.print("[red]Title must be between 1 and 200 characters[/red]")
            return

        # Create the task using the service
        task = service.add_task(title, description)
        console.print(f"[green]Task ban gaya![/green] (ID: {task.id})")
    except ValueError as e:
        console.print(f"[red]{str(e)}[/red]")
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")


@app.command()
def list():
    """
    List all tasks in a rich, colored table with emojis.
    """
    try:
        tasks = service.get_all_tasks()

        if not tasks:
            console.print("[yellow]Koi tasks nahi hain[/yellow]")
            return

        # Create a rich table
        table = Table(title="Task List", border_style="blue")
        table.add_column("ID", style="dim", width=36)  # UUID is 36 chars
        table.add_column("Status", style="bold")
        table.add_column("Title", style="bold")
        table.add_column("Description", style="italic")
        table.add_column("Created At", style="dim")

        for task in tasks:
            status = "✓ Done" if task.completed else "○ Pending"
            status_style = "green" if task.completed else "red"
            table.add_row(
                task.id,
                f"[{status_style}]{status}[/{status_style}]",
                task.title,
                task.description or "",
                task.created_at.strftime("%Y-%m-%d %H:%M:%S") if task.created_at else ""
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]An error occurred while listing tasks: {str(e)}[/red]")


@app.command()
def update(
    task_id: str = typer.Argument(..., help="ID of the task to update"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="New title for the task"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New description for the task")
):
    """
    Update a task by ID with new title and/or description.
    """
    try:
        # Update the task using the service
        updated_task = service.update_task(task_id, title=title, description=description)
        console.print(f"[green]Task update ho gaya![/green]")
    except ValueError as e:
        console.print(f"[red]{str(e)}[/red]")
    except Exception as e:
        console.print(f"[red]An error occurred while updating task: {str(e)}[/red]")


@app.command()
def delete(
    task_id: str = typer.Argument(..., help="ID of the task to delete")
):
    """
    Delete a task by ID.
    """
    try:
        # Delete the task using the service
        service.delete_task(task_id)
        console.print(f"[green]Task delete ho gaya![/green]")
    except ValueError as e:
        console.print(f"[red]{str(e)}[/red]")
    except Exception as e:
        console.print(f"[red]An error occurred while deleting task: {str(e)}[/red]")


@app.command()
def complete(
    task_id: str = typer.Argument(..., help="ID of the task to mark as complete")
):
    """
    Mark a task as complete by ID.
    """
    try:
        # Toggle the task status to complete using the service
        updated_task = service.toggle_task_status(task_id)
        console.print(f"[green]Task complete ho gaya![/green]")
    except ValueError as e:
        console.print(f"[red]{str(e)}[/red]")
    except Exception as e:
        console.print(f"[red]An error occurred while marking task complete: {str(e)}[/red]")


@app.command()
def incomplete(
    task_id: str = typer.Argument(..., help="ID of the task to mark as incomplete")
):
    """
    Mark a task as incomplete by ID.
    """
    try:
        # Toggle the task status to incomplete using the service
        updated_task = service.toggle_task_status(task_id)
        console.print(f"[green]Task incomplete ho gaya![/green]")
    except ValueError as e:
        console.print(f"[red]{str(e)}[/red]")
    except Exception as e:
        console.print(f"[red]An error occurred while marking task incomplete: {str(e)}[/red]")


if __name__ == "__main__":
    app()