'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { Bars3Icon, BellIcon, MoonIcon, SunIcon } from '@heroicons/react/24/outline';
import { UserCircleIcon } from '@heroicons/react/24/solid';

interface HeaderProps {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  onThemeToggle: () => void;
  isDarkMode: boolean;
}

export default function Header({ sidebarOpen, toggleSidebar, onThemeToggle, isDarkMode }: HeaderProps) {
  const [searchOpen, setSearchOpen] = useState(false);
  const pathname = usePathname();

  // Set theme based on user preference
  useEffect(() => {
    const root = document.documentElement;
    if (isDarkMode) {
      root.setAttribute('data-theme', 'dark');
    } else {
      root.removeAttribute('data-theme');
    }
  }, [isDarkMode]);

  return (
    <header className="sticky top-0 z-40 bg-surface border-b border-border shadow-sm">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Left side: Mobile menu button and breadcrumbs */}
        <div className="flex items-center gap-4">
          {toggleSidebar && (
            <button
              type="button"
              className="rounded-xl p-2 text-text-secondary hover:bg-surface-light hover:text-text-primary focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-200"
              onClick={toggleSidebar}
            >
              <span className="sr-only">Open sidebar</span>
              <Bars3Icon className="h-6 w-6" aria-hidden="true" />
            </button>
          )}

          {/* Breadcrumbs */}
          <nav className="hidden md:flex" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-3 text-sm">
              <li>
                <Link href="/" className="text-text-secondary hover:text-primary transition-colors">
                  Home
                </Link>
              </li>
              {pathname !== '/' && (
                <>
                  <li>
                    <span className="text-text-muted">/</span>
                  </li>
                  <li>
                    <Link
                      href={pathname}
                      className="capitalize text-text-secondary hover:text-primary transition-colors"
                    >
                      {pathname.split('/').pop() || 'Dashboard'}
                    </Link>
                  </li>
                </>
              )}
            </ol>
          </nav>
        </div>

        {/* Right side: Search, notifications, user profile, and theme toggle */}
        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="hidden md:block relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="h-5 w-5 text-text-muted" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
              </svg>
            </div>
            <input
              type="text"
              placeholder="Search tasks..."
              className="block w-48 pl-10 pr-3 py-2 bg-surface-light border border-border rounded-xl text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 text-sm shadow-sm"
            />
          </div>

          {/* Theme Toggle */}
          <button
            onClick={onThemeToggle}
            className="p-2 rounded-xl text-text-secondary hover:bg-surface-light hover:text-text-primary focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-200"
            aria-label={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            {isDarkMode ? (
              <SunIcon className="h-6 w-6 text-amber-400" />
            ) : (
              <MoonIcon className="h-6 w-6 text-text-secondary" />
            )}
          </button>

          {/* Notifications */}
          <button className="p-2 rounded-xl text-text-secondary hover:bg-surface-light hover:text-text-primary focus:outline-none focus:ring-2 focus:ring-primary relative transition-colors duration-200">
            <BellIcon className="h-6 w-6" />
            <span className="sr-only">View notifications</span>
            <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-error rounded-full"></span>
          </button>

          {/* User Profile */}
          <div className="relative ml-2">
            <div>
              <button
                type="button"
                className="flex rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                id="user-menu-button"
                aria-expanded="false"
                aria-haspopup="true"
              >
                <span className="sr-only">Open user menu</span>
                <div className="relative">
                  <UserCircleIcon className="h-9 w-9 text-primary" />
                  <span className="absolute bottom-0 right-0 block h-2.5 w-2.5 rounded-full ring-2 ring-surface bg-success"></span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile search bar */}
      <div className={`md:hidden px-4 pb-3 ${searchOpen ? 'block' : 'hidden'}`}>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg className="h-5 w-5 text-text-muted" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
            </svg>
          </div>
          <input
            type="text"
            placeholder="Search tasks..."
            className="block w-full pl-10 pr-3 py-2 bg-surface-light border border-border rounded-xl text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 text-sm"
          />
        </div>
      </div>
    </header>
  );
}