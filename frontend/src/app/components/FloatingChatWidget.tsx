'use client';

import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getStoredJwt } from '@/services/authService';

interface Message {
  role: string;
  content: string;
  type?: string;
  tasks?: any[];
}

// Function to process AI responses and ensure they follow the required guidelines
function processAIResponse(response: string): string {
  // Check if the response is unrelated to task management
  const unrelatedKeywords = [
    'joke', 'fun', 'game', 'movie', 'entertainment', 'weather', 'sports',
    'news', 'gossip', 'personal', 'private', 'secret', 'unrelated', 'off topic',
    'emoji', 'emoticon', 'smiley', 'casual', 'chill', 'relax', 'hang out'
  ];

  // Check if response contains unrelated content
  const lowerResponse = response.toLowerCase();
  const isUnrelated = unrelatedKeywords.some(keyword => lowerResponse.includes(keyword));

  if (isUnrelated) {
    return "I'm focused on helping you manage tasks and improve productivity. How can I assist with your tasks today?";
  }

  // Ensure response is concise and task-focused
  // If it's too long without clear task content, redirect to task management
  if (response.length > 300 && !lowerResponse.includes('task') &&
      !lowerResponse.includes('todo') && !lowerResponse.includes('productivity') &&
      !lowerResponse.includes('priority') && !lowerResponse.includes('deadline') &&
      !lowerResponse.includes('organize') && !lowerResponse.includes('schedule') &&
      !lowerResponse.includes('plan') && !lowerResponse.includes('goal')) {
    return "I'm here to help with your tasks and productivity. Could you tell me about a task you'd like to work on?";
  }

  // Ensure professional tone by removing any casual language
  let processedResponse = response
    .replace(/(hey|hi there|hello there|what's up|yo|dude|mate|buddy)/gi, 'Hello')
    .replace(/(cool|awesome|great|amazing)/gi, 'good')
    .replace(/\s:\)|:-\)|:D|xD|lol|rofl/g, '')
    .replace(/!\s*!\s*!/g, '!'); // Reduce excessive exclamation marks

  return processedResponse;
}

export default function FloatingChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I\'m your AI productivity assistant. How can I help you manage your tasks today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      // Get the JWT token
      const jwt = getStoredJwt();

      const headers: Record<string, string> = {
        'Content-Type': 'application/json'
      };

      // Add Authorization header if JWT token exists
      if (jwt) {
        headers['Authorization'] = `Bearer ${jwt}`;
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
        method: 'POST',
        headers,
        body: JSON.stringify({ message: input, locale: 'en' }),
        // Add timeout and other fetch options
        signal: AbortSignal.timeout(30000), // 30 second timeout
      });

      if (!response.ok) {
        const errorMessage = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorMessage}`);
      }

      const data = await response.json();
      const processedResponse = processAIResponse(data.response);

      if (data.tasks) {
        setMessages([
          ...newMessages,
          { role: 'assistant', content: processedResponse, type: 'tasks', tasks: data.tasks },
        ]);
      } else {
        setMessages([...newMessages, { role: 'assistant', content: processedResponse }]);
      }
    } catch (error: any) {
      console.error('Error sending message:', error);
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
        role: 'assistant',
        content: errorMessage
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <motion.div
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0, opacity: 0 }}
          className="w-80 h-96 bg-surface dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl shadow-xl flex flex-col overflow-hidden"
        >
          <div className="p-4 bg-gradient-to-r from-primary to-accent text-white">
            <div className="flex justify-between items-center">
              <h3 className="font-semibold text-lg">AI Assistant</h3>
              <button
                onClick={() => setIsOpen(false)}
                className="text-white hover:text-gray-200 transition-colors duration-200"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
          <div className="flex-1 p-4 overflow-y-auto bg-white dark:bg-gray-800">
            <div className="space-y-4">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl p-4 ${
                      msg.role === 'user'
                        ? 'bg-gradient-to-r from-primary to-accent text-white rounded-br-none shadow-md'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-none shadow-sm'
                    }`}
                  >
                    <div className="whitespace-pre-wrap">
                      {msg.content.split('\n').map((line, idx) => {
                        // Check if the line starts with a bullet point pattern
                        if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
                          return (
                            <div key={idx} className="flex items-start ml-4 my-1">
                              <span className="mr-2">•</span>
                              <span>{line.substring(2)}</span>
                            </div>
                          );
                        }
                        // Check if the line starts with a numbered list pattern
                        const numberedMatch = line.match(/^(\d+)\.\s(.*)/);
                        if (numberedMatch) {
                          return (
                            <div key={idx} className="flex items-start ml-4 my-1">
                              <span className="mr-2">{numberedMatch[1]}.</span>
                              <span>{numberedMatch[2]}</span>
                            </div>
                          );
                        }
                        return <div key={idx}>{line}</div>;
                      })}
                    </div>
                    {msg.type === 'tasks' && msg.tasks && Array.isArray(msg.tasks) && (
                      <div className="mt-3 space-y-2">
                        <div className="text-xs font-semibold border-t border-gray-300 dark:border-gray-600 pt-2 mt-2 text-gray-600 dark:text-gray-300">
                          Tasks:
                        </div>
                        {msg.tasks.map((task, taskIndex) => (
                          <div
                            key={taskIndex}
                            className="p-3 bg-white dark:bg-gray-600 rounded-lg border border-gray-200 dark:border-gray-600 text-xs shadow-sm"
                          >
                            <div className="font-medium text-gray-900 dark:text-white">{task.title}</div>
                            {task.description && <div className="text-gray-600 dark:text-gray-300 mt-1">{task.description}</div>}
                            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">ID: {task.id}</div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="max-w-[80%] rounded-2xl p-4 bg-gray-100 dark:bg-gray-700 rounded-bl-none shadow-sm">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 rounded-full bg-accent animate-bounce"></div>
                      <div className="w-2 h-2 rounded-full bg-accent animate-bounce delay-75"></div>
                      <div className="w-2 h-2 rounded-full bg-accent animate-bounce delay-150"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>
          <div className="p-3 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
            <div className="flex">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about your tasks..."
                className="flex-1 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white rounded-l-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent border border-gray-300 dark:border-gray-600 transition-all duration-200"
                disabled={isLoading}
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                className={`${
                  !input.trim() || isLoading
                    ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-primary to-accent hover:from-blue-600 hover:to-sky-500 text-white'
                } rounded-r-xl px-4 py-3 transition-all duration-300 shadow-md hover:shadow-lg`}
              >
                {isLoading ? (
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </button>
            </div>
          </div>
        </motion.div>
      ) : (
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setIsOpen(true)}
          className="w-14 h-14 rounded-full bg-gradient-to-r from-primary to-accent shadow-lg flex items-center justify-center text-white hover:shadow-xl transition-shadow duration-300"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </motion.button>
      )}
    </div>
  );
}