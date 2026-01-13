// Fixed Frontend API calls for your Next.js application

// Utility function to get JWT token from wherever you store it (localStorage, cookies, etc.)
const getAuthToken = () => {
  // Adjust this based on how you store your JWT token
  return localStorage.getItem('token'); // or however you retrieve your token
};

// API call to get all tasks
export const getAllTasks = async () => {
  try {
    const token = getAuthToken();
    
    const response = await fetch('/api/tasks/tasks', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const tasks = await response.json();
    return tasks;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
};

// API call to get a single task by ID
export const getTaskById = async (taskId) => {
  try {
    const token = getAuthToken();
    
    const response = await fetch(`/api/tasks/tasks/${taskId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const task = await response.json();
    return task;
  } catch (error) {
    console.error(`Error fetching task with ID ${taskId}:`, error);
    throw error;
  }
};

// Alternative Axios implementation (if you prefer axios)
import axios from 'axios';

const apiClient = axios.create({
  baseURL: '', // Base URL is empty since we're calling from Next.js frontend
});

// Request interceptor to add JWT token to all requests
apiClient.interceptors.request.use(
  (config) => {
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Using axios for getting all tasks
export const getAllTasksAxios = async () => {
  try {
    const response = await apiClient.get('/api/tasks/tasks');
    return response.data;
  } catch (error) {
    console.error('Error fetching tasks with axios:', error);
    throw error;
  }
};

// Using axios for getting a single task
export const getTaskByIdAxios = async (taskId) => {
  try {
    const response = await apiClient.get(`/api/tasks/tasks/${taskId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching task with ID ${taskId} with axios:`, error);
    throw error;
  }
};