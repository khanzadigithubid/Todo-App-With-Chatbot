'use client';

import { useState, useEffect } from 'react';
import { createTask, updateTask } from '@/services/api';
import { Task, TaskCreate } from '@/app/types/task';
import { useToast } from './ToastProvider';

interface TaskFormProps {
  refreshTasks: () => void;
  editingTask?: Task;
  onCloseEdit?: () => void;
}

export default function TaskForm({ refreshTasks, editingTask, onCloseEdit }: TaskFormProps) {
  const { showToast } = useToast();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [dueDate, setDueDate] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Populate form with editing task data
  useEffect(() => {
    if (editingTask) {
      setTitle(editingTask.title);
      setDescription(editingTask.description || '');
      setPriority(editingTask.priority as 'low' | 'medium' | 'high');
      setDueDate(editingTask.due_date || '');
    } else {
      // Reset form for new task
      setTitle('');
      setDescription('');
      setPriority('medium');
      setDueDate('');
    }
  }, [editingTask]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsLoading(true);
    try {
      if (editingTask) {
        // Update existing task
        await updateTask(editingTask.id, {
          title: title.trim(),
          description: description.trim(),
          priority,
          due_date: dueDate || undefined,
        });
        showToast('Task updated successfully', 'success');
        if (onCloseEdit) onCloseEdit();
      } else {
        // Create new task
        const newTask: TaskCreate = {
          title: title.trim(),
          description: description.trim(),
          priority,
          due_date: dueDate || undefined,
          status: 'pending',
        };

        await createTask(newTask);
        setTitle('');
        setDescription('');
        setPriority('medium');
        setDueDate('');
        showToast('Task created successfully', 'success');
      }

      refreshTasks();
    } catch (error) {
      console.error('Error saving task:', error);
      showToast(`Failed to ${editingTask ? 'update' : 'create'} task`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <label htmlFor="task-form-title-input" className="block text-sm font-medium text-text-primary mb-2">
          Task Title
        </label>
        <input
          id="task-form-title-input"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          className="w-full px-4 py-3 rounded-xl bg-surface-light border border-border placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all duration-200 text-text-primary"
          required
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-text-primary mb-2">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add details..."
          rows={3}
          className="w-full px-4 py-3 rounded-xl bg-surface-light border border-border placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all duration-200 text-text-primary"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div>
          <label htmlFor="priority" className="block text-sm font-medium text-text-primary mb-2">
            Priority
          </label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as 'low' | 'medium' | 'high')}
            className="w-full px-4 py-3 rounded-xl bg-surface-light border border-border focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all duration-200 text-text-primary"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div>
          <label htmlFor="dueDate" className="block text-sm font-medium text-text-primary mb-2">
            Due Date
          </label>
          <input
            id="dueDate"
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            className="w-full px-4 py-3 rounded-xl bg-surface-light border border-border focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all duration-200 text-text-primary"
          />
        </div>
      </div>

      <div className="flex justify-end gap-3">
        {editingTask && onCloseEdit && (
          <button
            type="button"
            onClick={onCloseEdit}
            className="px-5 py-2.5 rounded-xl font-semibold bg-surface-light text-text-secondary border border-border hover:bg-surface transition-all duration-300"
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          disabled={isLoading || !title.trim()}
          className={`px-5 py-2.5 rounded-xl font-semibold transition-all duration-300 ${
            isLoading || !title.trim()
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-primary to-accent hover:from-primary-light hover:to-accent text-white shadow-md hover:shadow-blue-lg'
          }`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {editingTask ? 'Updating...' : 'Creating...'}
            </span>
          ) : (
            editingTask ? 'Update Task' : 'Create Task'
          )}
        </button>
      </div>
    </form>
  );
}