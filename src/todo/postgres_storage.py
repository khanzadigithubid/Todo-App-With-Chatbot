from typing import Dict, List, Optional
from .models import Task
from uuid import uuid4
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PostgresStorage:
    """
    PostgreSQL storage implementation for storing tasks.
    """
    def __init__(self, connection_string: str = None):
        # Use the provided connection string or fall back to environment variable
        self.connection_string = (
            connection_string or 
            os.getenv('DATABASE_URL', 
                     'postgresql://neondb_owner:npg_klKz0pB4qaiQ@ep-young-dawn-a42wlho5-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
        )
        self._initialize_db()

    def _get_connection(self):
        """Get a database connection."""
        return psycopg2.connect(self.connection_string)

    def _initialize_db(self):
        """Initialize the database with the tasks table if it doesn't exist."""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id VARCHAR(36) PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT,
                        status VARCHAR(20) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()

    def add_task(self, task: Task) -> Task:
        """Add a task to PostgreSQL storage."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO tasks (id, title, description, status, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, title, description, status, created_at
                """, (task.id, task.title, task.description, task.status, task.created_at))
                
                result = cursor.fetchone()
                conn.commit()
                
                # Convert the result back to a Task object
                return Task(
                    id=result['id'],
                    title=result['title'],
                    description=result['description'],
                    status=result['status'],
                    created_at=result['created_at']
                )

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID from PostgreSQL storage."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT id, title, description, status, created_at
                    FROM tasks
                    WHERE id = %s
                """, (task_id,))
                
                result = cursor.fetchone()
                
                if result:
                    return Task(
                        id=result['id'],
                        title=result['title'],
                        description=result['description'],
                        status=result['status'],
                        created_at=result['created_at']
                    )
                return None

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from PostgreSQL storage."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT id, title, description, status, created_at
                    FROM tasks
                    ORDER BY created_at DESC
                """)
                
                results = cursor.fetchall()
                
                return [
                    Task(
                        id=row['id'],
                        title=row['title'],
                        description=row['description'],
                        status=row['status'],
                        created_at=row['created_at']
                    )
                    for row in results
                ]

    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Update a task by ID with provided attributes in PostgreSQL storage."""
        # Build the dynamic query based on provided kwargs
        set_parts = []
        params = []
        
        for key, value in kwargs.items():
            if hasattr(Task, key) and key != 'id':
                set_parts.append(f"{key} = %s")
                params.append(value)
        
        if not set_parts:
            # If no valid fields to update, just return the existing task
            return self.get_task(task_id)
        
        set_clause = ", ".join(set_parts)
        params.append(task_id)
        
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = f"""
                    UPDATE tasks
                    SET {set_clause}
                    WHERE id = %s
                    RETURNING id, title, description, status, created_at
                """
                
                cursor.execute(query, params)
                result = cursor.fetchone()
                conn.commit()
                
                if result:
                    return Task(
                        id=result['id'],
                        title=result['title'],
                        description=result['description'],
                        status=result['status'],
                        created_at=result['created_at']
                    )
                return None

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID from PostgreSQL storage."""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                conn.commit()
                
                # Return True if a row was affected (task was deleted)
                return cursor.rowcount > 0