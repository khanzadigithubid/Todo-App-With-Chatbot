// Utility function to handle authentication errors
export const handleAuthError = () => {
  // Remove stored tokens
  localStorage.removeItem('jwt');
  localStorage.removeItem('user_id');
  
  // Redirect to login page
  if (typeof window !== 'undefined') {
    window.location.href = '/login';
  }
};

// Function to check if response is an auth error
export const isAuthError = (error: any): boolean => {
  if (error && typeof error === 'object') {
    // Check if it's an ApiError with status 401
    if (error.status === 401) {
      return true;
    }
    // Check if it's a response-like object with status 401
    if (error.status === 401) {
      return true;
    }
  }
  return false;
};