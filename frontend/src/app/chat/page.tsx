"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { getStoredJwt } from '@/services/authService'; // Import the function to get stored JWT

// Define types for our messages
interface Message {
  role: string;
  content: string;
  type?: string;
  tasks?: any[];
}

// Since we're only supporting English, we don't need dynamic locale
export default function ChatPage() {
  const router = useRouter(); // Add router hook
  const locale = 'en'; // Hardcode to English
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hello! I'm your AI assistant. How can I help you with your tasks today?" }
  ]);
  const [input, setInput] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = false;
        recognitionRef.current.interimResults = false;
        recognitionRef.current.lang = "en-US";

        recognitionRef.current.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setInput(transcript);
          setIsListening(false);
        };

        recognitionRef.current.onerror = (event: any) => {
          console.error("Speech recognition error", event.error);
          setIsListening(false);
        };
      }
    }
  }, []);

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      // Get the JWT token using the same method as FloatingChatWidget
      const jwt = getStoredJwt();
      console.log("JWT Token:", jwt); // Debug log

      const headers: Record<string, string> = {
        "Content-Type": "application/json"
      };

      // Add Authorization header if JWT token exists
      if (jwt) {
        headers["Authorization"] = `Bearer ${jwt}`;
        console.log('Authorization header added');
      } else {
        console.log("No JWT token found"); // Debug log
      }

      // Determine the API base URL based on environment
      let API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

      // If no environment variable is set, try to determine from window.location
      if (!API_BASE_URL) {
        if (typeof window !== 'undefined') {
          const { origin } = window.location;
          // If we're on localhost, use the backend port
          if (origin.includes('localhost') || origin.includes('127.0.0.1')) {
            API_BASE_URL = 'http://127.0.0.1:8000';
          } else {
            // For production, use the same origin
            API_BASE_URL = origin;
          }
        } else {
          // Default fallback for SSR
          API_BASE_URL = 'http://127.0.0.1:8000';
        }
      }

      // Replace 0.0.0.0 with localhost for browser requests
      if (API_BASE_URL.includes('0.0.0.0')) {
        API_BASE_URL = API_BASE_URL.replace('0.0.0.0', 'localhost');
      }

      const response = await fetch(`${API_BASE_URL}/api/chat/`, {
        method: "POST",
        headers,
        body: JSON.stringify({ message: input, locale: locale }),
        // Add timeout and other fetch options
        signal: AbortSignal.timeout(30000), // 30 second timeout
      });

      if (!response.ok) {
        const errorMessage = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorMessage}`);
      }

      const data = await response.json();

      if (data.tasks) {
        setMessages([
          ...newMessages,
          { role: "assistant", content: data.response, type: "tasks", tasks: data.tasks },
        ]);
      } else {
        setMessages([...newMessages, { role: "assistant", content: data.response }]);
      }
    } catch (error: any) {
      console.error("Error sending message:", error);
      let errorMessage = 'Sorry, there was an error processing your request.';

      if (error.name === 'AbortError') {
        errorMessage = 'Request timed out. Please try again.';
      } else if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
        errorMessage = 'Unable to connect to the server. Please check your connection and ensure the backend is running.';
      } else if (error.message.includes('HTTP error')) {
        errorMessage = `Server error: ${error.message}`;
      }

      // Add error message to chat
      setMessages([...newMessages, {
        role: "assistant",
        content: errorMessage
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="min-h-screen bg-background text-primary">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 px-4 py-4 bg-surface border-b border-border">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-primary to-primary-light flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-xl">FT</span>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-primary to-primary-light bg-clip-text text-transparent">
              FlowTask AI Assistant
            </span>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => router.push('/dashboard')}
              className="px-5 py-2.5 rounded-xl bg-surface hover:bg-surface-light text-primary font-medium transition-all duration-200 border border-border shadow-sm"
            >
              Dashboard
            </button>
          </div>
        </div>
      </nav>

      {/* Spacer for fixed navigation */}
      <div className="h-20"></div>

      {/* Chat Container */}
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="bg-surface rounded-2xl shadow-xl border border-border overflow-hidden h-[calc(100vh-5rem)] flex flex-col">
          {/* Chat Header */}
          <div className="px-6 py-5 border-b border-border bg-surface-light">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">AI Assistant</h1>
                <p className="text-success font-medium">Always here to help</p>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-success animate-pulse"></div>
                <span className="text-sm text-text-secondary">Online</span>
              </div>
            </div>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-6 bg-background">
            {messages.length === 0 ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-col items-center justify-center h-full text-center text-text-secondary p-8"
              >
                <div className="mb-8 p-6 bg-surface-light rounded-full border border-border shadow-sm">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-primary">
                    <path d="M8 12H16M12 8V16M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <motion.h3
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="text-2xl font-bold text-text-primary mb-3"
                >
                  Welcome to AI Assistant
                </motion.h3>
                <motion.p
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                  className="text-lg max-w-md mb-8"
                >
                  Ask me about your tasks, productivity tips, or anything else you need help with.
                </motion.p>
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="grid grid-cols-1 gap-4 max-w-md w-full"
                >
                  <button
                    onClick={() => setInput("Show me my pending tasks")}
                    className="text-left p-5 bg-surface-light hover:bg-surface rounded-xl border border-border text-text-secondary transition-all duration-200 hover:shadow-sm text-lg font-medium"
                  >
                    Show me my pending tasks
                  </button>
                  <button
                    onClick={() => setInput("What's my most important task today?")}
                    className="text-left p-5 bg-surface-light hover:bg-surface rounded-xl border border-border text-text-secondary transition-all duration-200 hover:shadow-sm text-lg font-medium"
                  >
                    What's my most important task today?
                  </button>
                  <button
                    onClick={() => setInput("Help me organize my work")}
                    className="text-left p-5 bg-surface-light hover:bg-surface rounded-xl border border-border text-text-secondary transition-all duration-200 hover:shadow-sm text-lg font-medium"
                  >
                    Help me organize my work
                  </button>
                </motion.div>
              </motion.div>
            ) : (
              <div className="space-y-6">
                {messages.map((msg, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-[85%] rounded-2xl p-5 ${
                        msg.role === "user"
                          ? "bg-gradient-to-r from-primary to-accent text-white rounded-br-none chat-bubble user"
                          : "bg-surface-light text-text-primary rounded-bl-none chat-bubble assistant border border-border"
                      }`}
                    >
                      <div className="whitespace-pre-wrap text-lg">{msg.content}</div>
                      {msg.type === "tasks" && msg.tasks && Array.isArray(msg.tasks) && (
                        <div className="mt-4 space-y-3">
                          <div className="text-base font-semibold border-t border-border pt-4 mt-4 text-text-primary">
                            Tasks:
                          </div>
                          {msg.tasks.map((task, taskIndex) => (
                            <div
                              key={taskIndex}
                              className="p-4 bg-surface rounded-xl border border-border text-base"
                            >
                              <div className="font-semibold text-text-primary">{task.title}</div>
                              {task.description && <div className="text-text-secondary mt-2">{task.description}</div>}
                              <div className="text-sm text-text-muted mt-2">ID: {task.id}</div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}
                {isLoading && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex justify-start"
                  >
                    <div className="max-w-[85%] rounded-2xl p-5 bg-surface-light rounded-bl-none border border-border">
                      <div className="flex items-center space-x-3">
                        <div className="w-3 h-3 rounded-full bg-primary animate-bounce"></div>
                        <div className="w-3 h-3 rounded-full bg-primary animate-bounce delay-75"></div>
                        <div className="w-3 h-3 rounded-full bg-primary animate-bounce delay-150"></div>
                      </div>
                    </div>
                  </motion.div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Chat Input */}
          <div className="p-5 bg-surface-light border-t border-border">
            <div className="flex items-end gap-3">
              <div className="flex-1 relative">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  rows={1}
                  className="w-full px-5 py-4 pr-16 bg-surface border border-border rounded-xl text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary resize-none max-h-32 shadow-sm"
                  placeholder="Message AI Assistant..."
                />
                <div className="absolute right-3 top-3 flex gap-1">
                  <button
                    onClick={() => {
                      if (recognitionRef.current) {
                        if (isListening) {
                          recognitionRef.current.stop();
                          setIsListening(false);
                        } else {
                          recognitionRef.current.start();
                          setIsListening(true);
                        }
                      }
                    }}
                    className={`p-2.5 rounded-lg ${
                      isListening ? "bg-error text-white" : "text-text-secondary hover:text-text-primary hover:bg-surface-light"
                    } transition-colors`}
                  >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 17C14.7614 17 17 14.7614 17 12V6C17 3.23858 14.7614 1 12 1C9.23858 1 7 3.23858 7 6V12C7 14.7614 9.23858 17 12 17Z" stroke="currentColor" strokeWidth="2"/>
                      <path d="M9 12C9 13.6569 10.3431 15 12 15C13.6569 15 15 13.6569 15 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <path d="M6 21V19C6 17.3431 7.34315 16 9 16H15C16.6569 16 18 17.3431 18 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                  </button>
                </div>
              </div>
              <button
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                className={`p-4 rounded-xl ${
                  !input.trim() || isLoading
                    ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-primary to-accent hover:from-primary-light hover:to-accent text-white shadow-md hover:shadow-blue-lg'
                } transition-all duration-200 flex items-center justify-center`}
              >
                {isLoading ? (
                  <svg className="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : (
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}