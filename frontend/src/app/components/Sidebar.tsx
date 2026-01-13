'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import {
  HomeIcon,
  ClipboardDocumentListIcon,
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  UserIcon,
  ArrowRightStartOnRectangleIcon,
  UserGroupIcon,
  MoonIcon,
  SunIcon
} from '@heroicons/react/24/outline';

const navItems = [
  { name: 'Dashboard', icon: HomeIcon, href: '/dashboard' },
  { name: 'Tasks', icon: ClipboardDocumentListIcon, href: '/dashboard/tasks' },
  { name: 'AI Chatbot', icon: ChatBubbleLeftRightIcon, href: '/chat' },
  { name: 'Analytics', icon: ChartBarIcon, href: '/dashboard/analytics' },
  { name: 'Team', icon: UserGroupIcon, href: '/dashboard/team' },
  { name: 'Profile', icon: UserIcon, href: '/dashboard/profile' },
  { name: 'Settings', icon: Cog6ToothIcon, href: '/dashboard/settings' },
];

interface SidebarProps {
  isOpen: boolean;
  toggleSidebar: () => void;
  onThemeToggle: () => void;
  isDarkMode: boolean;
}

export default function Sidebar({ isOpen, toggleSidebar, onThemeToggle, isDarkMode }: SidebarProps) {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed inset-0 z-40 bg-black/50 lg:hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={toggleSidebar}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-surface border-r border-border flex flex-col shadow-xl ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0 lg:static lg:inset-0 transition-all duration-300`}
        initial={false}
        animate={{ x: isOpen ? 0 : '-100%' }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
      >
        {/* Logo */}
        <div className="flex items-center gap-4 p-5 border-b border-border">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-primary to-accent flex items-center justify-center shadow-md">
            <span className="text-white font-bold text-xl">FT</span>
          </div>
          <div className={`${isCollapsed ? 'hidden' : ''} transition-opacity duration-300`}>
            <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">FlowTask</h1>
            <p className="text-xs text-text-secondary">AI Productivity Suite</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-3 pt-5 overflow-y-auto">
          <ul className="space-y-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;

              return (
                <li key={item.name}>
                  <Link
                    href={item.href}
                    className={`group flex items-center gap-3 w-full p-3.5 rounded-xl transition-all duration-200 ${
                      isActive
                        ? 'bg-gradient-to-r from-primary/10 to-accent/10 text-primary shadow-sm border border-primary/20'
                        : 'text-text-secondary hover:bg-surface-light hover:text-primary hover:underline'
                    }`}
                  >
                    <item.icon className={`w-6 h-6 flex-shrink-0 ${isActive ? 'text-primary' : 'text-text-secondary'}`} />
                    <span className={`${isCollapsed ? 'hidden' : ''} text-sm font-medium transition-opacity duration-300`}>
                      {item.name}
                    </span>
                  </Link>
                </li>
              );
            })}

            {/* Theme Toggle */}
            <li className="mt-2">
              <button
                onClick={onThemeToggle}
                className="group flex items-center gap-3 w-full p-3.5 rounded-xl transition-all duration-200 text-text-secondary hover:bg-surface-light hover:text-primary"
              >
                <div className="p-1.5 rounded-lg bg-surface-light">
                  {isDarkMode ? (
                    <SunIcon className="w-5 h-5 flex-shrink-0 text-amber-500" />
                  ) : (
                    <MoonIcon className="w-5 h-5 flex-shrink-0 text-text-secondary" />
                  )}
                </div>
                <span className={`${isCollapsed ? 'hidden' : ''} text-sm font-medium transition-opacity duration-300`}>
                  {isDarkMode ? 'Light Mode' : 'Dark Mode'}
                </span>
              </button>
            </li>

            {/* Logout */}
            <li className="mt-4 pt-4 border-t border-border">
              <Link
                href="/logout"
                className="group flex items-center gap-3 w-full p-3.5 rounded-xl transition-all duration-200 text-text-secondary hover:bg-surface-light hover:text-error"
              >
                <div className="p-1.5 rounded-lg bg-surface-light">
                  <ArrowRightStartOnRectangleIcon className="w-5 h-5 flex-shrink-0 text-text-secondary" />
                </div>
                <span className={`${isCollapsed ? 'hidden' : ''} text-sm font-medium transition-opacity duration-300`}>
                  Logout
                </span>
              </Link>
            </li>
          </ul>
        </nav>

        {/* Collapsible toggle */}
        <div className="p-3 border-t border-border">
          <button
            onClick={toggleCollapse}
            className="w-full flex items-center justify-center p-3 rounded-xl bg-surface-light hover:bg-surface border border-border transition-all duration-200"
          >
            <div className="flex items-center justify-center">
              {isCollapsed ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-text-secondary" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    fillRule="evenodd"
                    d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-text-secondary" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    fillRule="evenodd"
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
              )}
              <span className={`ml-2 text-sm font-medium ${isCollapsed ? 'hidden' : ''} text-text-secondary transition-opacity duration-300`}>
                {isCollapsed ? 'Expand' : 'Collapse'}
              </span>
            </div>
          </button>
        </div>
      </motion.aside>
    </>
  );
}