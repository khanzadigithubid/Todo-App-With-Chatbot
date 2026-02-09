// frontend/src/components/TaskList.tsx

import { useState, useEffect } from 'react';
import api from '@/lib/api';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority?: string;
  category?: string;
  due_date?: string;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  userId: string;
}

export default function TaskList({ userId }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, [userId]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      // In a real implementation, we would fetch tasks for the specific user
      // For now, we'll use a placeholder
      const data = await api.taskApi.getTasks();
      setTasks(data.tasks || []);
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading tasks...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="task-list">
      <h2>Your Tasks</h2>
      {tasks.length === 0 ? (
        <p>No tasks found. Create your first task!</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <li key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
              <h3>{task.title}</h3>
              {task.description && <p>{task.description}</p>}
              <div className="task-meta">
                {task.priority && <span className={`priority ${task.priority}`}>{task.priority}</span>}
                {task.category && <span className="category">{task.category}</span>}
                {task.due_date && <span className="due-date">Due: {new Date(task.due_date).toLocaleDateString()}</span>}
              </div>
              <div className="task-actions">
                <button
                  onClick={() => toggleTaskCompletion(task.id)}
                  className={`completion-btn ${task.completed ? 'completed' : ''}`}
                >
                  {task.completed ? 'Completed' : 'Mark Complete'}
                </button>
                <button onClick={() => deleteTask(task.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );

  async function toggleTaskCompletion(taskId: string) {
    try {
      await api.taskApi.toggleTaskCompletion(taskId);
      // Refresh the task list
      fetchTasks();
    } catch (err) {
      console.error('Failed to toggle task completion:', err);
    }
  }

  async function deleteTask(taskId: string) {
    try {
      await api.taskApi.deleteTask(taskId);
      // Refresh the task list
      fetchTasks();
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  }
}