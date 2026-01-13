'use client';

import { useState } from 'react';
import { updateTask, deleteTask } from '@/services/api';
import { useToast } from './ToastProvider';

interface BulkActionsProps {
  selectedTaskIds: string[];
  refreshTasks: () => void;
  clearSelection: () => void;
}

export default function BulkActions({ selectedTaskIds, refreshTasks, clearSelection }: BulkActionsProps) {
  const { showToast } = useToast();
  const [isProcessing, setIsProcessing] = useState(false);

  const handleStatusUpdate = async (status: 'pending' | 'completed') => {
    if (selectedTaskIds.length === 0) return;

    setIsProcessing(true);
    try {
      // Update all selected tasks to the new status
      const updatePromises = selectedTaskIds.map(id =>
        updateTask(id, { status })
      );

      await Promise.all(updatePromises);
      refreshTasks();
      clearSelection();
      showToast(`${selectedTaskIds.length} task(s) updated successfully`, 'success');
    } catch (error) {
      console.error('Error updating tasks:', error);
      showToast('Failed to update tasks', 'error');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDelete = async () => {
    if (selectedTaskIds.length === 0) return;

    if (!confirm(`Are you sure you want to delete ${selectedTaskIds.length} task(s)?`)) {
      return;
    }

    setIsProcessing(true);
    try {
      // Delete all selected tasks
      const deletePromises = selectedTaskIds.map(id => deleteTask(id));

      await Promise.all(deletePromises);
      refreshTasks();
      clearSelection();
      showToast(`${selectedTaskIds.length} task(s) deleted successfully`, 'success');
    } catch (error) {
      console.error('Error deleting tasks:', error);
      showToast('Failed to delete tasks', 'error');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-wrap items-center gap-4 p-3 bg-surface-light rounded-xl border border-border">
      <div className="text-sm font-medium text-text-primary">
        {selectedTaskIds.length} {selectedTaskIds.length === 1 ? 'task' : 'tasks'} selected
      </div>

      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => handleStatusUpdate('completed')}
          disabled={isProcessing}
          className="px-4 py-2 text-sm rounded-lg bg-gradient-to-r from-success to-emerald-600 text-white hover:from-emerald-600 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md transition-all duration-200"
        >
          Mark Complete
        </button>

        <button
          onClick={() => handleStatusUpdate('pending')}
          disabled={isProcessing}
          className="px-4 py-2 text-sm rounded-lg bg-gradient-to-r from-warning to-yellow-600 text-white hover:from-amber-600 hover:to-yellow-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md transition-all duration-200"
        >
          Mark Pending
        </button>

        <button
          onClick={handleDelete}
          disabled={isProcessing}
          className="px-4 py-2 text-sm rounded-lg bg-gradient-to-r from-error to-rose-600 text-white hover:from-red-600 hover:to-rose-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md transition-all duration-200"
        >
          Delete Selected
        </button>

        <button
          onClick={clearSelection}
          disabled={isProcessing}
          className="px-4 py-2 text-sm rounded-lg bg-surface-light text-text-primary hover:bg-surface disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 border border-border"
        >
          Clear Selection
        </button>
      </div>
    </div>
  );
}