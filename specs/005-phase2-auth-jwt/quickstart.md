# Quickstart: Phase II - Better Auth + JWT Authentication

This document provides instructions on how to set up and run the authentication feature.

## Prerequisites

-   Node.js and npm installed
-   Python 3.13+ and uv installed
-   A Neon PostgreSQL database
-   A Better Auth account and project

## Setup

### Backend

1.  Navigate to the `backend` directory.
2.  Create a `.env` file and add the following:
    ```
    DATABASE_URL=your_neon_database_url
    BETTER_AUTH_SECRET=your_better_auth_secret
    ```
3.  Install the dependencies: `uv pip install -r requirements.txt`

### Frontend

1.  Navigate to the `frontend` directory.
2.  Create a `.env.local` file and add the following:
    ```
    NEXT_PUBLIC_BETTER_AUTH_PROJECT_ID=your_better_auth_project_id
    BETTER_AUTH_SECRET=your_better_auth_secret
    ```
3.  Install the dependencies: `npm install`

## Running the Application

### Backend

1.  Navigate to the `backend` directory.
2.  Run the application: `uvicorn app.main:app --reload`

### Frontend

1.  Navigate to the `frontend` directory.
2.  Run the application: `npm run dev`

Now you can access the application at `http://localhost:3000`.
