import { Task, TaskCreate, TaskUpdate } from '../app/types/task';
import { getStoredJwt, isTokenExpired } from './authService'; // Import the functions
import { handleAuthError } from '../utils/authHandler';

// Ensure NEXT_PUBLIC_ prefix for environment variables to be available in browser
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

// Helper function for API calls
export class ApiError extends Error {
    constructor(message: string, public status: number) {
        super(message);
    }
}

async function callApi<T>(
    endpoint: string,
    method: string,
    body?: any
): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    console.log(`Making API call to: ${url}`); // Log the actual URL being called

    const headers: HeadersInit = {
        'Content-Type': 'application/json',
    };

    const jwt = getStoredJwt();

    // Check if token exists and is not expired before making request
    if (jwt) {
        if (isTokenExpired(jwt)) {
            // Token is expired, handle auth error
            handleAuthError();
            throw new ApiError('Token has expired', 401);
        }

        headers['Authorization'] = `Bearer ${jwt}`;
    }

    try {
        const response = await fetch(url, {
            method,
            headers, // Use the modified headers
            body: body ? JSON.stringify(body) : undefined,
        });

        console.log(`API response status: ${response.status} for URL: ${url}`); // Log response status

        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch (e) {
                // If response is not JSON, use status text
                errorData = { detail: `API Error: ${response.statusText}` };
            }

            // Handle 401 Unauthorized - redirect to login
            if (response.status === 401) {
                handleAuthError();
                throw new ApiError(errorData.detail || `API Error: ${response.statusText}`, response.status);
            }

            throw new ApiError(errorData.detail || `API Error: ${response.statusText}`, response.status);
        }

        // Handle 204 No Content for delete operations
        if (response.status === 204) {
            return null as T;
        }

        return response.json();
    } catch (error) {
        // More specific error handling
        if (error instanceof TypeError) {
            if (error.message.includes('fetch')) {
                // This could be a CORS issue, network issue, or server not accessible
                console.error(`Fetch error for URL ${url}:`, error);
                throw new ApiError(`Network error: Failed to connect to the server at ${url}. Please check if the server is running and accessible.`, 0);
            } else {
                // Other TypeError
                console.error(`Type error for URL ${url}:`, error);
                throw new ApiError(`Request error: ${error.message}`, 0);
            }
        }

        // Re-throw other errors
        console.error(`Other error for URL ${url}:`, error);
        throw error;
    }
}

// Authentication API calls
export async function loginUser(email: string, password: string): Promise<{ access_token: string }> {
    const formBody = new URLSearchParams();
    formBody.append('username', email);
    formBody.append('password', password);

    const response = await fetch(`${API_BASE_URL}/api/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        },
        body: formBody.toString(),
    });

    if (!response.ok) {
        let errorData;
        try {
            errorData = await response.json();
        } catch (e) {
            errorData = { detail: `API Error: ${response.statusText}` };
        }
        throw new ApiError(errorData.detail || `API Error: ${response.statusText}`, response.status);
    }
    
    const data = await response.json();
    console.log('Login response:', data);
    return data;
}

export async function signupUser(email: string, password: string, name: string): Promise<{ access_token: string }> {
    const response = await fetch(`${API_BASE_URL}/api/signup`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
    });

    if (!response.ok) {
        let errorData;
        try {
            errorData = await response.json();
        } catch (e) {
            errorData = { detail: `API Error: ${response.statusText}` };
        }
        throw new ApiError(errorData.detail || `API Error: ${response.statusText}`, response.status);
    }

    const data = await response.json();
    console.log('Signup response:', data);
    return data;
}

// Task API calls
export async function getTasks(
    search?: string,
    filters?: {
        status?: Task['status'] | 'all';
        priority?: Task['priority'] | 'all';
        categories?: string[];
        created_after?: string;
        due_before?: string;
    }
): Promise<Task[]> {
    let endpoint = `/api/tasks/tasks`;
    const queryParams = new URLSearchParams();

    if (search) {
        queryParams.append('search', search);
    }
    if (filters) {
        if (filters.status && filters.status !== 'all') queryParams.append('status', filters.status);
        if (filters.priority && filters.priority !== 'all') queryParams.append('priority', filters.priority);
        if (filters.categories && filters.categories.length > 0) queryParams.append('categories', filters.categories.join(','));
        if (filters.created_after) queryParams.append('created_after', filters.created_after);
        if (filters.due_before) queryParams.append('due_before', filters.due_before);
    }

    if (queryParams.toString()) {
        endpoint += `?${queryParams.toString()}`;
    }

    return callApi<Task[]>(endpoint, 'GET');
}

export async function createTask(task: TaskCreate): Promise<Task> {
    return callApi<Task>(`/api/tasks/tasks`, 'POST', task);
}

export async function updateTask(taskId: string, task: TaskUpdate): Promise<Task> {
    return callApi<Task>(`/api/tasks/tasks/${taskId}`, 'PUT', task);
}

export async function deleteTask(taskId: string): Promise<void> {
    return callApi<void>((`/api/tasks/tasks/${taskId}`), 'DELETE');
}

export async function toggleTaskCompletion(taskId: string): Promise<Task> {
    // Fetch the current task
    const task = await callApi<Task>(`/api/tasks/tasks/${taskId}`, 'GET');
    // Update the status by calling PUT
    return callApi<Task>(`/api/tasks/tasks/${taskId}`, 'PUT', {
        ...task,
        status: task.status === 'completed' ? 'pending' : 'completed'
    });
}

export async function bulkDeleteTasks(taskIds: string[]): Promise<void> {
    // Since backend doesn't support bulk delete, delete each task individually
    const deletePromises = taskIds.map(taskId =>
        callApi<void>(`/api/tasks/tasks/${taskId}`, 'DELETE')
    );
    await Promise.all(deletePromises);
}

export async function bulkToggleTaskCompletion(taskIds: string[], status: 'pending' | 'completed'): Promise<Task[]> {
    // Since backend doesn't support bulk toggle, toggle each task individually
    const promises = taskIds.map(taskId =>
        callApi<Task>(`/api/tasks/tasks/${taskId}`, 'PUT', { status })
    );
    return Promise.all(promises);
}

export async function exportTasks(format: 'json' | 'csv'): Promise<any> {
    // Since backend doesn't support export, fetch all tasks and format on frontend
    const tasks = await getTasks();
    if (format === 'json') {
        return JSON.stringify(tasks, null, 2);
    } else { // CSV
        if (!tasks || tasks.length === 0) return '';

        // Create CSV header from task keys
        const headers = Object.keys(tasks[0]);
        const csvHeader = headers.join(',');

        // Create CSV rows
        const csvRows = tasks.map(task => {
            return headers.map(header => {
                // Handle potential commas or quotes in values
                const value = task[header as keyof typeof task];
                return typeof value === 'string' && value.includes(',') ? `"${value}"` : value;
            }).join(',');
        });

        return [csvHeader, ...csvRows].join('\n');
    }
}