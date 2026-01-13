# Instructions to Fix Frontend API Calls

## Issue Identified
The frontend is calling `/api/users/tasks` which doesn't exist on your backend. Your backend has the following routes:
- GET `/api/tasks/tasks` → Read Tasks
- GET `/api/tasks/tasks/{task_id}` → Read single Task

## Solution Steps

### 1. Update API Call Functions
Replace your existing API call functions with the ones provided in `frontend_api_fix.js`. Specifically:

- Change `fetch('/api/users/tasks')` to `fetch('/api/tasks/tasks')`
- Ensure JWT token is properly added to the Authorization header as `Bearer {token}`

### 2. Update Your Components
Find all instances in your Next.js components where you're calling the API and update them:

```javascript
// OLD (causing 404):
const response = await fetch('/api/users/tasks', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

// NEW (correct):
const response = await fetch('/api/tasks/tasks', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

### 3. Token Retrieval
Make sure your JWT token is properly retrieved from storage (localStorage, cookies, etc.) and formatted correctly as `Bearer {token}` in the Authorization header.

### 4. Error Handling
Update your error handling to account for the new routes and ensure proper error responses are handled.

### 5. Testing
After making these changes:
1. Test that the API calls now return 200 OK instead of 404
2. Verify that tasks are properly displayed in your UI
3. Check that individual task retrieval works correctly

## Additional Notes
- The token must be sent in the Authorization header as `Bearer {your-jwt-token}`
- Make sure your authentication middleware on the backend is properly configured to accept the token
- If you're using SWR or React Query, update the endpoint URLs in those configurations as well