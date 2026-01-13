'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode';
import { motion } from 'framer-motion';
import {
  CalendarDaysIcon,
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  ChartBarIcon,
  UserGroupIcon,
  Cog6ToothIcon,
  ArrowRightStartOnRectangleIcon
} from '@heroicons/react/24/outline';
import { getStoredJwt, isTokenExpired } from '@/services/authService';
import { getTasks, ApiError } from '@/services/api';
import { Task } from '@/app/types/task';
import Header from '../components/Header';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import SearchBar from '../components/SearchBar';
import FilterDropdown from '../components/FilterDropdown';
import StatsCard from '../components/StatsCard';
import BulkActions from '../components/BulkActions';
import FloatingChatWidget from '../components/FloatingChatWidget';
import { ToastProvider } from '../components/ToastProvider';

// Helper function to normalize task to ensure categories is always an array
function normalizeTask(task: Task): Task {
  return {
    ...task,
    categories: Array.isArray(task.categories) ? task.categories : (task.categories || []),
  };
}

// Helper function to normalize an array of tasks
function normalizeTasks(tasks: Task[]): Task[] {
  return tasks.map(normalizeTask);
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [userId, setUserId] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [filterParams, setFilterParams] = useState<{ status?: string; priority?: string }>({});
  const [selectedTaskIds, setSelectedTaskIds] = useState<string[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsDarkMode(true);
      document.documentElement.setAttribute('data-theme', 'dark');
    }

    const token = getStoredJwt();
    if (token) {
      if (isTokenExpired(token)) {
        // Token is expired, remove it and redirect to login
        localStorage.removeItem('jwt');
        localStorage.removeItem('user_id');
        router.push('/login');
        return;
      }

      try {
        const decoded: { sub: string } = jwtDecode(token);
        setUserId(decoded.sub);
      } catch (error) {
        console.error('Invalid token:', error);
        router.push('/login');
      }
    } else {
      router.push('/login');
    }
  }, [router]);

  const fetchTasks = useCallback(async () => {
    if (userId) {
      try {
        const fetchedTasks = await getTasks();
        setTasks(Array.isArray(fetchedTasks) ? normalizeTasks(fetchedTasks) : []);
      } catch (error) {
        console.error('Error fetching tasks:', error);
        if (error instanceof ApiError && error.status === 404) {
          localStorage.removeItem('user_id');
          router.push('/login');
        }
      }
    }
  }, [userId, router]);

  useEffect(() => {
    if (userId) {
      fetchTasks();
    }
  }, [userId, fetchTasks]);

  const handleSearch = (query: string) => {
    setSearchTerm(query);
  };

  const handleFilterChange = (filters: { status?: string; priority?: string }) => {
    setFilterParams(filters);
  };

  const handleSelectedTasksChange = (selectedIds: string[]) => {
    setSelectedTaskIds(selectedIds);
  };

  const clearSelectedTasks = () => {
    setSelectedTaskIds([]);
  };

  const filteredTasks = normalizeTasks(tasks)
    .filter(task => {
      const searchTermLower = searchTerm.toLowerCase();
      return task.title.toLowerCase().includes(searchTermLower) ||
             task.description?.toLowerCase().includes(searchTermLower);
    })
    .filter(task => {
      if (filterParams.status && task.status !== filterParams.status) {
        return false;
      }
      if (filterParams.priority && task.priority !== filterParams.priority) {
        return false;
      }
      return true;
    });

  // Calculate task statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.status === 'completed').length;
  const pendingTasks = tasks.filter(task => task.status === 'pending').length;
  const highPriorityTasks = tasks.filter(task => task.priority === 'high').length;
  const overdueTasks = tasks.filter(task => {
    if (!task.due_date) return false;
    return new Date(task.due_date) < new Date();
  }).length;

  const toggleTheme = () => {
    const newTheme = !isDarkMode;
    setIsDarkMode(newTheme);
    localStorage.setItem('theme', newTheme ? 'dark' : 'light');

    if (newTheme) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  };

  if (!userId) {
    return (
      <div className="flex justify-center items-center min-h-[calc(100vh-4rem)] bg-background">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mb-4"></div>
          <p className="text-text-secondary">Loading user session...</p>
        </div>
      </div>
    );
  }

  return (
    <ToastProvider>
      <div className="flex flex-col min-h-screen bg-background">
        {/* Header */}
        <Header
          sidebarOpen={false}
          toggleSidebar={() => {}}
          onThemeToggle={toggleTheme}
          isDarkMode={isDarkMode}
        />

        <div className="flex flex-1">
          {/* Main content area */}
          <main className="flex-1 overflow-y-auto py-8 px-4 sm:px-6">
            <div className="max-w-7xl w-full mx-auto">
              {/* Page title and action buttons */}
              <div className="mb-10">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
                  <div>
                    <motion.h1
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent"
                    >
                      Dashboard
                    </motion.h1>
                    <motion.p
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 }}
                      className="mt-2 text-lg text-text-secondary"
                    >
                      Welcome back! Here's what's happening with your tasks today.
                    </motion.p>
                  </div>
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.2 }}
                  >
                    <button
                      type="button"
                      onClick={() => document.getElementById('task-form-title-input')?.focus()}
                      className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-primary to-accent hover:from-primary-light hover:to-accent text-white font-bold transition-all duration-300 flex items-center gap-3 text-base shadow-md hover:shadow-blue-lg"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                          clipRule="evenodd"
                        />
                      </svg>
                      <span>New Task</span>
                    </button>
                  </motion.div>
                </div>
              </div>

              {/* Stats cards */}
              <motion.div
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <StatsCard
                  key={`stats-total-${totalTasks}`}
                  title="Total Tasks"
                  value={totalTasks}
                  subtitle="All tasks assigned to you"
                  icon={<CalendarDaysIcon className="w-6 h-6 text-white" />}
                  variant="primary"
                />
                <StatsCard
                  key={`stats-completed-${completedTasks}`}
                  title="Completed"
                  value={completedTasks}
                  subtitle="Tasks you've finished"
                  icon={<CheckCircleIcon className="w-6 h-6 text-white" />}
                  variant="success"
                />
                <StatsCard
                  key={`stats-pending-${pendingTasks}`}
                  title="Pending"
                  value={pendingTasks}
                  subtitle="Tasks awaiting completion"
                  icon={<ClockIcon className="w-6 h-6 text-white" />}
                  variant="warning"
                />
                <StatsCard
                  key={`stats-overdue-${overdueTasks}`}
                  title="Overdue"
                  value={overdueTasks}
                  subtitle="Tasks past due date"
                  icon={<ExclamationTriangleIcon className="w-6 h-6 text-white" />}
                  variant="danger"
                />
              </motion.div>

              {/* Task summary and actions */}
              <div className="grid grid-cols-1 gap-8">
                {/* Task creation form */}
                <motion.div
                  className="w-full"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  <div className="bg-surface rounded-2xl shadow-lg border border-border">
                    <div className="px-6 py-5 border-b border-border bg-surface-light">
                      <div className="flex items-center gap-5">
                        <div className="w-14 h-14 rounded-xl bg-gradient-to-r from-primary to-accent flex items-center justify-center shadow-md">
                          <svg
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                            className="text-white"
                          >
                            <path
                              d="M12 6V4M12 18V16M5.63604 18.364L4.22183 19.7782M6.36396 5.63604L4.94975 4.22183M19.7782 5.63604L18.364 4.22183M18.364 19.7782L19.7782 18.364M20 12H22M2 12H4M16.9497 7.05025L15.5355 5.63604M16.9497 16.9497L15.5355 18.364"
                              stroke="currentColor"
                              strokeWidth="2"
                              strokeLinecap="round"
                              strokeLinejoin="round"
                            />
                          </svg>
                        </div>
                        <div>
                          <h2 className="text-2xl font-bold text-text-primary">Create New Task</h2>
                          <p className="text-text-secondary">Add a new task to your list</p>
                        </div>
                      </div>
                    </div>
                    <div className="p-6">
                      <TaskForm refreshTasks={fetchTasks} />
                    </div>
                  </div>
                </motion.div>

                {/* Task list and filters */}
                <motion.div
                  className="w-full"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                >
                  <div className="bg-surface rounded-2xl shadow-lg border border-border">
                    <div className="px-6 py-5 border-b border-border bg-surface-light">
                      <div className="flex flex-col sm:flex-row items-center justify-between gap-5">
                        <div>
                          <h2 className="text-2xl font-bold text-text-primary">Your Tasks</h2>
                          <p className="text-text-secondary">Manage your tasks efficiently</p>
                        </div>
                        <div className="w-full sm:w-auto flex flex-col sm:flex-row gap-4">
                          <SearchBar onSearch={handleSearch} />
                          <FilterDropdown onFilterChange={handleFilterChange} />
                        </div>
                      </div>
                    </div>
                    <div className="p-6">
                      {selectedTaskIds.length > 0 && (
                        <motion.div
                          className="bg-surface-light rounded-xl p-4 border border-border mb-6"
                          initial={{ opacity: 0, scale: 0.95 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ duration: 0.3 }}
                        >
                          <BulkActions
                            selectedTaskIds={selectedTaskIds}
                            refreshTasks={() => {
                              fetchTasks();
                              clearSelectedTasks();
                            }}
                            clearSelection={clearSelectedTasks}
                          />
                        </motion.div>
                      )}

                      <TaskList
                        key={`task-list-${filteredTasks.length}`}
                        tasks={filteredTasks}
                        refreshTasks={fetchTasks}
                        selectedTaskIds={selectedTaskIds}
                        onSelectedTasksChange={handleSelectedTasksChange}
                      />
                    </div>
                  </div>
                </motion.div>
              </div>
            </div>
          </main>

          {/* Floating Chat Widget */}
          <FloatingChatWidget />
        </div>
      </div>
    </ToastProvider>
  );
}