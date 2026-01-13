'use client';

import { useState, useRef, useEffect } from 'react';

interface FilterDropdownProps {
  onFilterChange: (filters: { status?: string; priority?: string }) => void;
}

export default function FilterDropdown({ onFilterChange }: FilterDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  useEffect(() => {
    onFilterChange({
      status: statusFilter === 'all' ? undefined : statusFilter,
      priority: priorityFilter === 'all' ? undefined : priorityFilter
    });
  }, [statusFilter, priorityFilter, onFilterChange]);

  const handleStatusChange = (value: string) => {
    setStatusFilter(value);
  };

  const handlePriorityChange = (value: string) => {
    setPriorityFilter(value);
  };

  const clearFilters = () => {
    setStatusFilter('all');
    setPriorityFilter('all');
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center px-4 py-2.5 border border-border rounded-xl shadow-sm text-sm font-medium text-text-primary bg-surface-light hover:bg-surface focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-200"
      >
        <svg className="-ml-1 mr-2 h-5 w-5 text-text-muted" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clipRule="evenodd" />
        </svg>
        Filters
      </button>

      {isOpen && (
        <div className="origin-top-right absolute right-0 mt-2 w-64 rounded-xl shadow-xl bg-surface ring-1 ring-border z-50 overflow-hidden">
          <div className="py-1">
            <div className="px-4 py-3">
              <h3 className="text-sm font-semibold text-text-primary mb-3">Status</h3>
              <div className="space-y-2">
                {['all', 'pending', 'completed'].map((status) => (
                  <div key={status} className="flex items-center">
                    <input
                      id={`status-${status}`}
                      name="status"
                      type="radio"
                      checked={statusFilter === status}
                      onChange={() => handleStatusChange(status)}
                      className="h-4 w-4 text-accent focus:ring-accent border-border bg-surface-light"
                    />
                    <label htmlFor={`status-${status}`} className="ml-3 block text-sm text-text-primary capitalize">
                      {status}
                    </label>
                  </div>
                ))}
              </div>
            </div>

            <div className="px-4 py-3 border-t border-border">
              <h3 className="text-sm font-semibold text-text-primary mb-3">Priority</h3>
              <div className="space-y-2">
                {['all', 'low', 'medium', 'high'].map((priority) => (
                  <div key={priority} className="flex items-center">
                    <input
                      id={`priority-${priority}`}
                      name="priority"
                      type="radio"
                      checked={priorityFilter === priority}
                      onChange={() => handlePriorityChange(priority)}
                      className="h-4 w-4 text-accent focus:ring-accent border-border bg-surface-light"
                    />
                    <label htmlFor={`priority-${priority}`} className="ml-3 block text-sm text-text-primary capitalize">
                      {priority}
                    </label>
                  </div>
                ))}
              </div>
            </div>

            <div className="px-4 py-3 border-t border-border flex justify-between">
              <button
                onClick={clearFilters}
                className="text-sm font-medium text-error hover:text-error/80 transition-colors duration-200"
              >
                Clear
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="text-sm font-medium text-accent hover:text-accent-light transition-colors duration-200"
              >
                Apply
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}