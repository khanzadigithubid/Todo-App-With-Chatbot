'use client';

import { useState, useEffect, createContext, useContext, ReactNode } from 'react';

type ToastType = 'success' | 'error' | 'warning' | 'info';

interface ToastContextType {
  showToast: (message: string, type: ToastType) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

interface ToastProviderProps {
  children: ReactNode;
}

export const ToastProvider = ({ children }: ToastProviderProps) => {
  const [toast, setToast] = useState<{ message: string; type: ToastType; id: number } | null>(null);

  const showToast = (message: string, type: ToastType) => {
    const id = Date.now();
    setToast({ message, type, id });
  };

  useEffect(() => {
    if (toast) {
      const timer = setTimeout(() => {
        setToast(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [toast]);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {toast && (
        <div className={`toast ${toast.type} fixed top-4 right-4 p-4 rounded-xl shadow-xl z-50 transform transition-all duration-300 ease-in-out`}>
          <div className="flex items-center">
            {toast.type === 'success' && (
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-100/30 dark:bg-green-900/30 flex items-center justify-center mr-3">
                <svg className="w-4 h-4 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
            )}
            {toast.type === 'error' && (
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-error/10 dark:bg-red-900/30 flex items-center justify-center mr-3">
                <svg className="w-4 h-4 text-error" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </div>
            )}
            {toast.type === 'warning' && (
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-warning/10 dark:bg-amber-900/30 flex items-center justify-center mr-3">
                <svg className="w-4 h-4 text-warning" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
              </div>
            )}
            {toast.type === 'info' && (
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/10 dark:bg-blue-900/30 flex items-center justify-center mr-3">
                <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            )}
            <span className="text-sm font-medium text-text-primary">{toast.message}</span>
          </div>
        </div>
      )}
    </ToastContext.Provider>
  );
};