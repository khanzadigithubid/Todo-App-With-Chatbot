"use client";

import { useState, useRef, useEffect } from "react";

// Define types for our messages
interface Message {
  role: string;
  content: string;
  type?: string;
  tasks?: any[];
}

// Since this is a client component in a dynamic route, we need to receive the locale as a prop
// The locale will be passed from the parent layout
export default function ChatPage({ params }: { params: { locale: string } }) {
  const locale = params.locale || 'en'; // Get locale from props
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = false;
        recognitionRef.current.interimResults = false;
        // Set the speech recognition language based on the locale
        recognitionRef.current.lang = locale === "ur" ? "ur-PK" : "en-US";

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
  }, [locale]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input, locale: locale }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
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
    } catch (error) {
      console.error("Error sending message:", error);
      // Add error message to chat
      setMessages([...newMessages, {
        role: "assistant",
        content: "Sorry, there was an error processing your request. Please make sure the backend server is running."
      }]);
    }
  };

  const handleMicClick = () => {
    if (recognitionRef.current) {
      if (isListening) {
        recognitionRef.current.stop();
        setIsListening(false);
      } else {
        recognitionRef.current.start();
        setIsListening(true);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900">
      <div className="flex-1 p-4 overflow-y-auto">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex mb-4 ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`rounded-lg p-3 max-w-lg ${
                msg.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white"
              }`}
            >
              {msg.content}
              {msg.type === "tasks" && msg.tasks && Array.isArray(msg.tasks) && (
                <ul className="mt-2">
                  {msg.tasks.map((task) => (
                    <li key={task.id} className="mt-1 p-2 border-t border-gray-300 dark:border-gray-600">
                      <strong>{task.title}</strong>
                      <p className="text-sm">{task.description}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">ID: {task.id}</p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        ))}
      </div>
      <div className="p-4 bg-white dark:bg-gray-800">
        <div className="flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            className="flex-1 p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            placeholder="Type your message..."
          />
          <button
            onClick={handleMicClick}
            className={`ml-2 px-4 py-2 rounded-lg ${
              isListening ? "bg-red-500" : "bg-gray-500"
            } text-white`}
          >
            🎤
          </button>
          <button
            onClick={handleSend}
            className="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}