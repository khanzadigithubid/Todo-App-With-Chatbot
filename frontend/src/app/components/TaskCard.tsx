'use client';

import { useState } from 'react';
import { deleteTask, toggleTaskCompletion } from '@/services/api';
import { Task } from '../types/task';
import TaskForm from './TaskForm';
import { useToast } from './ToastProvider';
import EditIcon from './icons/EditIcon';
import DeleteIcon from './icons/DeleteIcon';
import { motion } from 'framer-motion';

interface TaskCardProps {
  task: Task;
  refreshTasks: () => void;
  onSelectToggle?: (taskId: string) => void;
  isSelected?: boolean;
}

export default function TaskCard({ task, refreshTasks, onSelectToggle, isSelected }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const { showToast } = useToast();

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(task.id);
        showToast('Task deleted successfully!', 'success');
        refreshTasks();
      } catch (error: any) {
        showToast(`Error deleting task: ${error.message}`, 'error');
      }
    }
  };

  const handleToggleComplete = async () => {
    try {
      await toggleTaskCompletion(task.id);
      showToast(`Task marked ${task.status === 'completed' ? 'pending' : 'completed'}!`, 'success');
      refreshTasks();
    } catch (error: any) {
      showToast(`Error updating task status: ${error.message}`, 'error');
    }
  };

  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return 'No due date';
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  // Define priority colors for the new aesthetic
  const priorityColors = {
    high: 'bg-gradient-to-r from-rose-500/20 to-red-500/20 text-rose-500 border border-rose-500/30',
    medium: 'bg-gradient-to-r from-amber-500/20 to-yellow-500/20 text-amber-500 border border-amber-500/30',
    low: 'bg-gradient-to-r from-emerald-500/20 to-green-500/20 text-emerald-500 border border-emerald-500/30'
  };

  // Define priority icons
  const priorityIcons = {
    high: '🔴',
    medium: '🟡',
    low: '🟢'
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      whileHover={{ y: -5 }}
      className={`
        relative p-6 bg-surface rounded-2xl border border-border shadow-sm
        hover:shadow-lg hover:shadow-purple/50
        transition-all duration-300
        ${task.status === 'completed' ? 'opacity-80 bg-surface-light' : ''}
        overflow-hidden
        group
      `}
    >
      {isEditing ? (
        <TaskForm
          refreshTasks={() => {
            setIsEditing(false);
            refreshTasks();
          }}
          editingTask={task}
          onCloseEdit={() => setIsEditing(false)}
        />
      ) : (
        <>
          {/* Task Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-start gap-3 flex-grow">
              {onSelectToggle && (
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => onSelectToggle(task.id)}
                  className="mt-1.5 w-5 h-5 rounded border-border text-primary focus:ring-primary focus:ring-offset-0"
                />
              )}
              <div className="flex-grow">
                <div className="flex items-center gap-2.5 mb-2">
                  <span className="text-lg">{priorityIcons[task.priority as keyof typeof priorityIcons]}</span>
                  <h3 className={`text-lg font-bold ${task.status === 'completed' ? 'line-through text-text-muted' : 'text-primary'}`}>
                    {task.title}
                  </h3>
                </div>
                {task.description && (
                  <p className="text-text-secondary text-base leading-relaxed mb-3">
                    {task.description}
                  </p>
                )}
              </div>
            </div>
            <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                onClick={() => setIsEditing(true)}
                className="p-2 rounded-lg bg-surface-light hover:bg-surface-light/80 transition-colors border border-border"
                aria-label="Edit task"
              >
                <EditIcon className="w-4 h-4 text-text-secondary hover:text-primary" />
              </button>
              <button
                onClick={handleDelete}
                className="p-2 rounded-lg bg-surface-light hover:bg-surface-light/80 transition-colors border border-border"
                aria-label="Delete task"
              >
                <DeleteIcon className="w-4 h-4 text-text-secondary hover:text-error" />
              </button>
            </div>
          </div>

          {/* Task Details */}
          <div className="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-border">
            <div className="flex flex-wrap items-center gap-3">
              {/* Due Date */}
              {task.due_date && (
                <div className="flex items-center gap-2">
                  <div className="p-2 rounded-lg bg-surface-light">
                    <span className="text-text-secondary text-sm">📅</span>
                  </div>
                  <span className="text-text-secondary text-sm">{formatDate(task.due_date)}</span>
                </div>
              )}

              {/* Priority */}
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-lg bg-surface-light">
                  <span className="text-text-secondary text-sm">⚡</span>
                </div>
                <div className={`px-3 py-1 rounded-full text-sm font-semibold ${priorityColors[task.priority as keyof typeof priorityColors]}`}>
                  {task.priority}
                </div>
              </div>

              {/* Categories */}
              {task.categories && Array.isArray(task.categories) && task.categories.length > 0 && (
                <div className="flex items-center gap-2">
                  <div className="p-2 rounded-lg bg-surface-light">
                    <span className="text-text-secondary text-sm">#️⃣</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {task.categories.map((cat, index) => {
                      if (!cat) return null; // Skip if cat is null/undefined
                      return (
                        <span
                          key={`${task.id}-${index}`} // Using task.id and index as key to ensure uniqueness
                          className="px-2.5 py-1 bg-surface-light rounded-full text-sm font-medium text-text-secondary border border-border"
                        >
                          {cat}
                        </span>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>

            {/* Status Toggle */}
            <div className="flex items-center gap-2">
              <span className={`text-sm font-medium ${task.status === 'completed' ? 'text-success' : 'text-text-secondary'}`}>
                {task.status === 'completed' ? 'Done' : 'Pending'}
              </span>
              <input
                type="checkbox"
                checked={task.status === 'completed'}
                onChange={handleToggleComplete}
                className="w-5 h-5 rounded border-border text-primary focus:ring-primary focus:ring-offset-0"
              />
            </div>
          </div>
        </>
      )}
    </motion.div>
  );
}