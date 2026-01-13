"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { motion } from "framer-motion";
import { SunIcon, MoonIcon } from "@heroicons/react/24/outline";

export default function HomePage() {
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

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

  const handleLoginClick = () => {
    router.push("/login");
  };

  const handleSignupClick = () => {
    router.push("/signup");
  };

  return (
    <div className="min-h-screen bg-background text-text-primary">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 px-4 py-4 bg-surface border-b border-border">
        <div className="container mx-auto flex justify-between items-center">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="flex items-center gap-3"
          >
            <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-primary to-accent flex items-center justify-center shadow-md">
              <span className="text-white font-bold text-xl">FT</span>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              FlowTask
            </span>
          </motion.div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => router.push("/dashboard")}
              className="px-5 py-2.5 rounded-xl bg-surface hover:bg-surface-light text-text-primary font-medium transition-all duration-200 border border-border shadow-sm"
            >
              Dashboard
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleLoginClick}
              className="px-5 py-2.5 rounded-xl bg-surface hover:bg-surface-light text-text-primary font-medium transition-all duration-200 border border-border shadow-sm"
            >
              Login
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSignupClick}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent hover:from-primary-light hover:to-accent text-white font-medium transition-all duration-200 shadow-md hover:shadow-blue-lg"
            >
              Sign Up
            </motion.button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="z-50 text-text-primary p-2"
              aria-label={isMenuOpen ? "Close menu" : "Open menu"}
            >
              {isMenuOpen ? (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              ) : (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
              )}
            </button>
          </div>
        </div>
      </nav>

      {/* Spacer for fixed navigation */}
      <div className="h-20"></div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="md:hidden fixed top-0 left-0 w-full h-screen bg-surface z-40 flex flex-col"
        >
          <div className="w-full max-w-md p-6 mx-auto">
            <div className="space-y-4">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => {
                  router.push("/dashboard");
                  setIsMenuOpen(false);
                }}
                className="w-full text-left px-5 py-3.5 rounded-xl bg-surface-light hover:bg-surface text-text-primary font-medium transition-all duration-200 border border-border shadow-sm"
              >
                Dashboard
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => {
                  handleLoginClick();
                  setIsMenuOpen(false);
                }}
                className="w-full text-left px-5 py-3.5 rounded-xl bg-surface-light hover:bg-surface text-text-primary font-medium transition-all duration-200 border border-border shadow-sm"
              >
                Login
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => {
                  handleSignupClick();
                  setIsMenuOpen(false);
                }}
                className="w-full text-left px-5 py-3.5 rounded-xl bg-gradient-to-r from-primary to-accent hover:from-primary-light hover:to-accent text-white font-medium transition-all duration-200 shadow-md hover:shadow-blue-lg"
              >
                Sign Up
              </motion.button>
            </div>
          </div>
        </motion.div>
      )}

      {/* Hero Section */}
      <main className="relative z-10 px-4 py-16">
        <div className="container mx-auto max-w-7xl">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-center lg:text-left"
            >
              <motion.div
                className="inline-block mb-6"
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.6, type: "spring", stiffness: 100 }}
              >
                <span className="px-4 py-2 rounded-full bg-surface-light text-text-secondary text-sm font-medium border border-border shadow-sm">
                  AI-Powered Productivity
                </span>
              </motion.div>

              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
                <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">FlowTask</span>
                <br />
                <span className="text-text-primary">Plan Smarter. Execute Faster.</span>
              </h1>

              <p className="text-xl text-text-secondary mb-10 max-w-2xl mx-auto lg:mx-0">
                Manage your tasks, stay organized, and get intelligent assistance to focus on what truly matters — all in one smart platform.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-5">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleSignupClick}
                  className="px-8 py-4 rounded-xl bg-gradient-to-r from-primary to-accent hover:from-primary-light hover:to-accent text-white font-bold transition-all duration-300 shadow-lg hover:shadow-blue-lg flex items-center gap-3"
                >
                  <span>Get Started Free</span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => router.push("/dashboard")}
                  className="px-8 py-4 rounded-xl text-text-primary font-medium transition-all duration-200 border border-border hover:bg-surface-light"
                >
                  Explore Features
                </motion.button>
              </div>

              <div className="mt-10 flex flex-wrap justify-center lg:justify-start gap-8">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-success flex items-center justify-center shadow-sm">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </div>
                  <span className="text-text-secondary font-medium">No credit card required</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-success flex items-center justify-center shadow-sm">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </div>
                  <span className="text-text-secondary font-medium">Free 14-day trial</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-success flex items-center justify-center shadow-sm">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </div>
                  <span className="text-text-secondary font-medium">Cancel anytime</span>
                </div>
              </div>
            </motion.div>

            <div className="flex justify-center items-center">
              <div className="relative w-full max-w-lg">
                <div className="rounded-2xl overflow-hidden border border-border bg-surface shadow-xl">
                  <div className="p-6">
                    <div className="flex justify-between items-center mb-6">
                      <div className="text-lg font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">FlowTask Dashboard</div>
                      <div className="flex space-x-2">
                        <div className="w-3 h-3 rounded-full bg-rose-500"></div>
                        <div className="w-3 h-3 rounded-full bg-amber-500"></div>
                        <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                      </div>
                    </div>

                    <div className="space-y-5">
                      <div className="p-5 bg-surface-light rounded-xl border border-border shadow-sm">
                        <div className="flex justify-between items-center">
                          <div className="font-semibold text-text-primary">Prepare quarterly report</div>
                          <div className="text-xs text-success font-medium">AI Scheduled</div>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2.5 mt-3">
                          <div className="bg-success h-2.5 rounded-full" style={{ width: '100%' }}></div>
                        </div>
                      </div>

                      <div className="p-5 bg-surface-light rounded-xl border border-border shadow-sm">
                        <div className="flex justify-between items-center">
                          <div className="font-semibold text-text-primary">Team sync meeting</div>
                          <div className="text-xs text-success font-medium">AI Delegated</div>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2.5 mt-3">
                          <div className="bg-success h-2.5 rounded-full" style={{ width: '75%' }}></div>
                        </div>
                      </div>

                      <div className="p-5 bg-surface-light rounded-xl border border-border shadow-sm">
                        <div className="flex justify-between items-center">
                          <div className="font-semibold text-text-primary">Budget review</div>
                          <div className="text-xs text-success font-medium">AI Optimized</div>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2.5 mt-3">
                          <div className="bg-success h-2.5 rounded-full" style={{ width: '45%' }}></div>
                        </div>
                      </div>
                    </div>

                    <div className="mt-7 pt-6 border-t border-border">
                      <div className="flex items-center justify-between">
                        <div className="text-text-secondary font-medium">Tasks Automated</div>
                        <div className="text-xl font-bold text-text-primary">12/15</div>
                      </div>
                      <div className="mt-3 flex items-center justify-between">
                        <div className="text-text-secondary font-medium">Time Saved</div>
                        <div className="text-lg font-bold text-text-primary">8h 30m</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Key Features Section */}
      <section className="relative z-10 py-20 bg-surface-light">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-text-primary">
              Powerful Productivity Features
            </h2>
            <p className="text-xl text-text-secondary">
              Everything you need to streamline your workflow and boost efficiency
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
            {[
              {
                title: "Smart Prioritization",
                description: "AI-powered prioritization based on deadlines and importance",
                icon: "⚡"
              },
              {
                title: "Team Collaboration",
                description: "Real-time collaboration with your team members",
                icon: "👥"
              },
              {
                title: "Intelligent Insights",
                description: "Actionable analytics to improve your productivity",
                icon: "📊"
              },
              {
                title: "Cross-Platform Sync",
                description: "Access your work from any device, anywhere",
                icon: "🔄"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * index, duration: 0.5 }}
                className="p-7 bg-surface rounded-2xl border border-border shadow-sm hover:shadow-md transition-all duration-300 group"
              >
                <div className="text-5xl mb-5 group-hover:scale-110 transition-transform duration-300">{feature.icon}</div>
                <h3 className="text-xl font-bold text-text-primary mb-3">{feature.title}</h3>
                <p className="text-text-secondary">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="relative z-10 py-20">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
            {[
              { value: "95%", label: "Productivity Increase", description: "of users report improved efficiency" },
              { value: "40%", label: "Time Saved", description: "on average per week" },
              { value: "10k+", label: "Active Users", description: "across industries" },
              { value: "24/7", label: "Support", description: "availability for our customers" }
            ].map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 * index, duration: 0.5 }}
                className="p-7 bg-surface rounded-2xl border border-border shadow-sm hover:shadow-md transition-all duration-300 text-center"
              >
                <div className="text-4xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent mb-3">{stat.value}</div>
                <h3 className="text-xl font-bold text-text-primary mb-3">{stat.label}</h3>
                <p className="text-text-secondary">{stat.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 py-20 bg-surface-light">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="bg-surface rounded-2xl border border-border shadow-lg text-center p-12"
            >
              <div className="inline-block mb-6">
                <span className="px-4 py-2 rounded-full bg-surface-light text-text-secondary text-sm font-medium border border-border shadow-sm">
                  Transform Your Productivity
                </span>
              </div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6 text-text-primary">
                Ready to Transform Your Productivity?
              </h2>
              <p className="text-xl text-text-secondary mb-10 max-w-2xl mx-auto">
                Join thousands of professionals who have transformed their workflow with our productivity platform.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-5">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleSignupClick}
                  className="px-8 py-4 rounded-xl bg-gradient-to-r from-primary to-accent hover:from-primary-light hover:to-accent text-white font-bold transition-all duration-300 shadow-lg hover:shadow-blue-lg flex items-center gap-3"
                >
                  <span>Start Free Trial</span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleLoginClick}
                  className="px-8 py-4 rounded-xl text-text-primary font-medium transition-all duration-200 border border-border hover:bg-surface-light"
                >
                  Sign In
                </motion.button>
              </div>
              <div className="mt-8 flex flex-wrap justify-center gap-8 text-text-secondary">
                <div className="flex items-center gap-3">
                  <svg className="w-5 h-5 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span className="font-medium">No credit card required</span>
                </div>
                <div className="flex items-center gap-3">
                  <svg className="w-5 h-5 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span className="font-medium">14-day free trial</span>
                </div>
                <div className="flex items-center gap-3">
                  <svg className="w-5 h-5 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span className="font-medium">Cancel anytime</span>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 px-4 py-12 border-t border-border">
        <div className="container mx-auto max-w-7xl">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-primary to-accent flex items-center justify-center shadow-md">
                  <span className="text-white font-bold text-lg">FT</span>
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                  FlowTask
                </span>
              </div>
              <p className="text-text-secondary mb-6">
                The AI-powered productivity platform that helps teams streamline their workflow and boost efficiency.
              </p>
              <div className="flex space-x-5">
                <a href="#" className="text-text-secondary hover:text-accent transition-colors">
                  <span className="sr-only">Twitter</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.008 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>
                  </svg>
                </a>
                <a href="#" className="text-text-secondary hover:text-accent transition-colors">
                  <span className="sr-only">GitHub</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd"></path>
                  </svg>
                </a>
                <a href="#" className="text-text-secondary hover:text-accent transition-colors">
                  <span className="sr-only">LinkedIn</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" clipRule="evenodd"></path>
                  </svg>
                </a>
              </div>
            </div>
            <div>
              <h3 className="text-lg font-bold text-text-primary mb-6">Solutions</h3>
              <ul className="space-y-4">
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">Project Management</a></li>
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">Team Collaboration</a></li>
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">Resource Planning</a></li>
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">Reporting</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold text-text-primary mb-6">Support</h3>
              <ul className="space-y-4">
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">Pricing</a></li>
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">Documentation</a></li>
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">Guides</a></li>
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">API Status</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold text-text-primary mb-6">Company</h3>
              <ul className="space-y-4">
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">About</a></li>
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">Blog</a></li>
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">Jobs</a></li>
                <li><a href="#" className="text-text-secondary hover:text-accent transition-colors">Press</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-16 pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center">
            <p className="text-text-secondary">&copy; 2023 FlowTask. All rights reserved.</p>
            <div className="mt-4 md:mt-0 flex space-x-8">
              <a href="#" className="text-text-secondary hover:text-accent transition-colors">Privacy Policy</a>
              <a href="#" className="text-text-secondary hover:text-accent transition-colors">Terms of Service</a>
              <a href="#" className="text-text-secondary hover:text-accent transition-colors">Cookie Policy</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}