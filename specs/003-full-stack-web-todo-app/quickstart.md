# Quickstart: Full-Stack Web Todo App

This document provides instructions on how to set up and run the project.

## Prerequisites

- Python 3.13+
- Node.js 18+
- `uv` package installed (`pip install uv`)
- A Neon Serverless PostgreSQL database

## Setup

1.  **Clone the repository.**
2.  **Create a `.env` file** in the root of the project and add your Neon database connection string:
    ```
    DATABASE_URL="postgresql://user:password@host:port/dbname"
    ```
3.  **Backend Setup:**
    ```bash
    cd backend
    uv venv
    uv pip install -r requirements.txt
    ```
4.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install
    ```

## Running the Application

1.  **Start the backend server:**
    ```bash
    cd backend
    uv run uvicorn app.main:app --reload
    ```
2.  **Start the frontend development server:**
    ```bash
    cd frontend
    npm run dev
    ```

The application will be available at `http://localhost:3000`.
