'use client';

import { useEffect } from 'react';
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline';

interface DarkModeToggleProps {
  isDarkMode: boolean;
  toggleTheme: () => void;
}

export default function DarkModeToggle({ isDarkMode, toggleTheme }: DarkModeToggleProps) {
  useEffect(() => {
    const root = document.documentElement;
    if (isDarkMode) {
      root.setAttribute('data-theme', 'dark');
    } else {
      root.removeAttribute('data-theme');
    }
  }, [isDarkMode]);

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-accent"
      aria-label={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
    >
      {isDarkMode ? (
        <SunIcon className="h-5 w-5" />
      ) : (
        <MoonIcon className="h-5 w-5" />
      )}
    </button>
  );
}