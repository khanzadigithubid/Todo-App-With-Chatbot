import { ReactNode } from 'react';

interface StatsCardProps {
  title: string;
  value: number | string;
  subtitle: string;
  icon: ReactNode;
  variant: 'primary' | 'success' | 'warning' | 'danger';
}

export default function StatsCard({ title, value, subtitle, icon, variant }: StatsCardProps) {
  const variantClasses = {
    primary: 'bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 text-blue-800 dark:text-blue-200 border border-blue-100 dark:border-blue-800/50',
    success: 'bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/30 dark:to-emerald-900/30 text-green-800 dark:text-green-200 border border-green-100 dark:border-green-800/50',
    warning: 'bg-gradient-to-br from-amber-50 to-yellow-50 dark:from-amber-900/30 dark:to-yellow-900/30 text-amber-800 dark:text-amber-200 border border-amber-100 dark:border-amber-800/50',
    danger: 'bg-gradient-to-br from-red-50 to-rose-50 dark:from-red-900/30 dark:to-rose-900/30 text-red-800 dark:text-red-200 border border-red-100 dark:border-red-800/50',
  };

  const iconBgClasses = {
    primary: 'bg-gradient-to-r from-blue-500 to-indigo-600',
    success: 'bg-gradient-to-r from-green-500 to-emerald-600',
    warning: 'bg-gradient-to-r from-amber-500 to-yellow-600',
    danger: 'bg-gradient-to-r from-red-500 to-rose-600',
  };

  return (
    <div className={`bg-surface rounded-2xl shadow-md p-6 ${variantClasses[variant]} transition-transform duration-300 hover:scale-[1.02]`}>
      <div className="flex items-center justify-between">
        <div>
          <div className="text-text-secondary text-sm font-medium">{title}</div>
          <div className="text-3xl font-bold text-text-primary mt-1">{value}</div>
          <div className="text-text-muted text-xs mt-2">{subtitle}</div>
        </div>
        <div className={`${iconBgClasses[variant]} w-14 h-14 rounded-xl flex items-center justify-center shadow-lg`}>
          {icon}
        </div>
      </div>
    </div>
  );
}