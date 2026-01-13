# Todo App Backend

This is the backend API for the Todo App, built with FastAPI.

## Deployment

### For Hugging Face Spaces

To deploy this backend on Hugging Face Spaces, you'll need:

1. A `Dockerfile` or Python environment with the dependencies in `requirements.txt`
2. Environment variables:
   - `BETTER_AUTH_SECRET`: A strong secret key for JWT authentication
   - `DATABASE_URL`: Database connection string (optional, defaults to local SQLite)

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Health check
- `POST /api/token` - User login
- `POST /api/users/` - User registration
- `GET/POST/PUT/DELETE /api/users/tasks` - Task management endpoints
- `GET/POST /api/chat` - Chat endpoints