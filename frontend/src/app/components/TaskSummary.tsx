import { Task } from '@/app/types/task';

interface TaskSummaryProps {
  tasks: Task[];
}

export default function TaskSummary({ tasks }: TaskSummaryProps) {
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.status === 'completed').length;
  const pendingTasks = tasks.filter(task => task.status === 'pending').length;
  const highPriorityTasks = tasks.filter(task => task.priority === 'high').length;
  const overdueTasks = tasks.filter(task => {
    if (!task.due_date) return false;
    return new Date(task.due_date) < new Date();
  }).length;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
        <div className="text-2xl font-semibold text-accent">{totalTasks}</div>
        <div className="text-sm text-gray-600">Total Tasks</div>
      </div>
      <div className="bg-success/10 p-4 rounded-lg border border-success">
        <div className="text-2xl font-semibold text-success">{completedTasks}</div>
        <div className="text-sm text-gray-600">Completed</div>
      </div>
      <div className="bg-amber-100 p-4 rounded-lg border border-amber-500">
        <div className="text-2xl font-semibold text-amber-800">{pendingTasks}</div>
        <div className="text-sm text-gray-600">Pending</div>
      </div>
      <div className="bg-error/10 p-4 rounded-lg border border-error">
        <div className="text-2xl font-semibold text-error">{overdueTasks}</div>
        <div className="text-sm text-gray-600">Overdue</div>
      </div>
    </div>
  );
}