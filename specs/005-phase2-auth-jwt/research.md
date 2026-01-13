# Research: Phase II - Better Auth + JWT Authentication

This document outlines the research required to implement authentication using Better Auth and JWT in the full-stack application.

## 1. Better Auth with Next.js App Router

**Decision**: We will use the official Better Auth React library and follow their documentation for Next.js 13+ App Router integration.

**Rationale**: The official library is the most reliable and up-to-date solution for integrating Better Auth with a Next.js application. Their documentation will provide the necessary components and hooks for creating signup and login forms.

**Alternatives considered**:
- Building a custom solution: This would be time-consuming and prone to security vulnerabilities.

## 2. Better Auth JWT Plugin

**Decision**: We will enable the JWT plugin in the Better Auth dashboard for our project.

**Rationale**: The JWT plugin is a built-in feature of Better Auth that allows for the creation of JWTs upon user login. This is the most straightforward way to get the required tokens.

**Alternatives considered**:
- Generating our own JWTs: This would add unnecessary complexity and potential security risks.

## 3. FastAPI JWT Middleware

**Decision**: We will create a custom middleware in FastAPI using `PyJWT` to protect our task-related endpoints.

**Rationale**: A custom middleware will give us the flexibility to implement our specific authentication logic, such as extracting the `user_id` from the token and verifying it against the URL path.

**Alternatives considered**:
- Using a third-party library: While there are libraries that can simplify JWT authentication in FastAPI, a custom middleware will be more explicit and easier to tailor to our needs.

**Implementation Outline**:
```python
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path not in ["/api/signup", "/api/login"]: # Unprotected routes
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Unauthorized")

            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, "YOUR_SECRET_KEY", algorithms=["HS256"])
                request.state.user_id = payload.get("user_id")
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")

        response = await call_next(request)
        return response
```

## 4. Shared Secret Management

**Decision**: The `BETTER_AUTH_SECRET` will be stored in an `.env` file in both the `frontend` and `backend` directories.

**Rationale**: Using environment variables is a standard and secure way to manage secrets in development. For production, we would use a more secure secret management solution.

**Alternatives considered**:
- Hardcoding the secret: This is a major security risk and should never be done.

## 5. PyJWT Usage

**Decision**: We will use the `PyJWT` library in our FastAPI backend to decode and verify the JWTs issued by Better Auth.

**Rationale**: `PyJWT` is the standard library for working with JWTs in Python and is well-maintained and widely used.

**Alternatives considered**:
- Implementing our own JWT logic: This is complex and not recommended.
