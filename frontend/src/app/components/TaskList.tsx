'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TrashIcon, PencilIcon, CheckCircleIcon, ClockIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';
import { Task } from '@/app/types/task';
import { deleteTask, updateTask } from '@/services/api';
import { useToast } from './ToastProvider';

interface TaskListProps {
  tasks: Task[];
  refreshTasks: () => void;
  selectedTaskIds: string[];
  onSelectedTasksChange: (selectedIds: string[]) => void;
}

export default function TaskList({ tasks, refreshTasks, selectedTaskIds, onSelectedTasksChange }: TaskListProps) {
  const { showToast } = useToast();
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  const handleDelete = async (taskId: string) => {
    try {
      await deleteTask(taskId);
      refreshTasks();
      showToast('Task deleted successfully', 'success');
    } catch (error) {
      console.error('Error deleting task:', error);
      showToast('Failed to delete task', 'error');
    }
  };

  const handleStatusToggle = async (task: Task) => {
    try {
      await updateTask(task.id, {
        ...task,
        status: task.status === 'completed' ? 'pending' : 'completed'
      });
      refreshTasks();
      showToast(`Task marked as ${task.status === 'completed' ? 'pending' : 'completed'}`, 'success');
    } catch (error) {
      console.error('Error updating task status:', error);
      showToast('Failed to update task status', 'error');
    }
  };

  const startEditing = (task: Task) => {
    setEditingTaskId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
  };

  const saveEdit = async () => {
    if (!editingTaskId) return;

    try {
      await updateTask(editingTaskId, {
        title: editTitle,
        description: editDescription
      });
      setEditingTaskId(null);
      refreshTasks();
      showToast('Task updated successfully', 'success');
    } catch (error) {
      console.error('Error updating task:', error);
      showToast('Failed to update task', 'error');
    }
  };

  const cancelEdit = () => {
    setEditingTaskId(null);
  };

  const handleSelectTask = (taskId: string) => {
    if (selectedTaskIds.includes(taskId)) {
      onSelectedTasksChange(selectedTaskIds.filter(id => id !== taskId));
    } else {
      onSelectedTasksChange([...selectedTaskIds, taskId]);
    }
  };

  const handleSelectAll = () => {
    if (selectedTaskIds.length === tasks.length) {
      onSelectedTasksChange([]);
    } else {
      onSelectedTasksChange(tasks.map(task => task.id));
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="w-5 h-5 text-success" />;
      case 'pending':
        return <ClockIcon className="w-5 h-5 text-amber-500" />;
      default:
        return <ExclamationTriangleIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-gradient-to-r from-red-100 to-rose-100 dark:from-red-900/30 dark:to-rose-900/30 text-red-800 dark:text-red-200';
      case 'medium':
        return 'bg-gradient-to-r from-amber-100 to-yellow-100 dark:from-amber-900/30 dark:to-yellow-900/30 text-amber-800 dark:text-amber-200';
      case 'low':
        return 'bg-gradient-to-r from-green-100 to-emerald-100 dark:from-green-900/30 dark:to-emerald-900/30 text-green-800 dark:text-green-200';
      default:
        return 'bg-gradient-to-r from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 text-gray-800 dark:text-gray-200';
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-border">
        <thead className="bg-surface-light">
          <tr>
            <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-text-primary uppercase tracking-wider w-12">
              <input
                type="checkbox"
                checked={selectedTaskIds.length === tasks.length && tasks.length > 0}
                onChange={handleSelectAll}
                className="h-4 w-4 text-accent focus:ring-accent border-border rounded bg-surface-light"
              />
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-text-primary uppercase tracking-wider">
              Task
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-text-primary uppercase tracking-wider">
              Status
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-text-primary uppercase tracking-wider">
              Priority
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-text-primary uppercase tracking-wider">
              Due Date
            </th>
            <th scope="col" className="px-6 py-4 text-right text-xs font-semibold text-text-primary uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-surface divide-y divide-border">
          <AnimatePresence>
            {tasks.map((task) => (
              <motion.tr
                key={task.id}
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.2 }}
                className={`hover:bg-surface-light transition-colors duration-200 ${selectedTaskIds.includes(task.id) ? 'bg-blue-50/30' : ''}`}
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <input
                    type="checkbox"
                    checked={selectedTaskIds.includes(task.id)}
                    onChange={() => handleSelectTask(task.id)}
                    className="h-4 w-4 text-accent focus:ring-accent border-border rounded bg-surface-light"
                  />
                </td>
                <td className="px-6 py-4">
                  {editingTaskId === task.id ? (
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="w-full px-4 py-2 rounded-lg border border-border focus:ring-2 focus:ring-accent focus:border-primary bg-surface-light text-text-primary"
                      />
                      <textarea
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                        className="w-full px-4 py-2 rounded-lg border border-border focus:ring-2 focus:ring-accent focus:border-primary bg-surface-light text-text-primary"
                        rows={2}
                      />
                      <div className="flex space-x-3 mt-2">
                        <button
                          onClick={saveEdit}
                          className="px-4 py-2 bg-gradient-to-r from-primary to-accent text-white rounded-lg text-sm font-medium hover:from-primary-light hover:to-accent transition-all duration-300 shadow-md hover:shadow-blue-lg"
                        >
                          Save
                        </button>
                        <button
                          onClick={cancelEdit}
                          className="px-4 py-2 bg-surface-light text-text-primary rounded-lg text-sm font-medium hover:bg-surface transition-colors"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div>
                      <div className="font-semibold text-text-primary">{task.title}</div>
                      {task.description && (
                        <div className="text-sm text-text-secondary mt-1">{task.description}</div>
                      )}
                    </div>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    {getStatusIcon(task.status)}
                    <span className="ml-2 capitalize text-sm font-medium text-text-primary">{task.status}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-3 py-1.5 text-xs font-semibold rounded-full ${getPriorityColor(task.priority)} shadow-sm`}>
                    {task.priority}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-text-secondary">
                  {task.due_date ? new Date(task.due_date).toLocaleDateString() : (
                    <span className="text-text-muted italic">No due date</span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex justify-end space-x-2">
                    <button
                      onClick={() => handleStatusToggle(task)}
                      className="text-text-secondary hover:text-primary p-2 rounded-lg hover:bg-surface-light transition-colors duration-200"
                      title={task.status === 'completed' ? 'Mark as pending' : 'Mark as completed'}
                    >
                      {task.status === 'completed' ? (
                        <ClockIcon className="w-5 h-5" />
                      ) : (
                        <CheckCircleIcon className="w-5 h-5" />
                      )}
                    </button>
                    <button
                      onClick={() => startEditing(task)}
                      className="text-text-secondary hover:text-primary p-2 rounded-lg hover:bg-surface-light transition-colors duration-200"
                      title="Edit task"
                    >
                      <PencilIcon className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(task.id)}
                      className="text-text-secondary hover:text-error p-2 rounded-lg hover:bg-surface-light transition-colors duration-200"
                      title="Delete task"
                    >
                      <TrashIcon className="w-5 h-5" />
                    </button>
                  </div>
                </td>
              </motion.tr>
            ))}
          </AnimatePresence>
        </tbody>
      </table>

      {tasks.length === 0 && (
        <div className="text-center py-16">
          <div className="mx-auto w-24 h-24 rounded-2xl bg-gradient-to-br from-blue-100 to-indigo-100 dark:from-blue-900/30 dark:to-indigo-900/30 flex items-center justify-center mb-6">
            <svg className="w-12 h-12 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
            </svg>
          </div>
          <h3 className="text-xl font-bold text-text-primary mb-2">No tasks yet</h3>
          <p className="text-text-secondary max-w-md mx-auto">
            Get started by creating a new task. Your tasks will appear here once added.
          </p>
          <div className="mt-6">
            <button
              type="button"
              onClick={() => document.getElementById('task-form-title-input')?.focus()}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent hover:from-primary-light hover:to-accent text-white font-semibold transition-all duration-300 shadow-md hover:shadow-blue-lg"
            >
              Create Your First Task
            </button>
          </div>
        </div>
      )}
    </div>
  );
}