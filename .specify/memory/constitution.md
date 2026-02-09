# Hackathon II: Todo App - Constitution

## Project Overview
This is a monorepo using GitHub Spec-Kit for spec-driven development of a Todo application that evolves from a simple console app to a cloud-native AI chatbot deployed on Kubernetes.

## Core Values
1. **Spec-Driven Development**: All code must map to a validated specification
2. **Clean Architecture**: Maintain clear separation of concerns
3. **Security First**: Implement proper authentication and authorization
4. **Scalability**: Design for horizontal scaling from the start
5. **AI-First**: Integrate AI capabilities thoughtfully throughout

## Technology Stack Constraints
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI, SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- AI: OpenAI Agents SDK, MCP SDK
- Infrastructure: Docker, Kubernetes, Helm Charts
- Event Streaming: Kafka or Redpanda
- Service Mesh: Dapr

## Security Requirements
- All API endpoints must require JWT authentication
- Never store secrets in code
- Use environment variables for sensitive data
- Implement proper input validation
- Sanitize all user inputs

## Performance Expectations
- API responses under 500ms
- Frontend bundle size under 250KB
- Database queries optimized with proper indexing
- Caching implemented for frequently accessed data

## Code Quality Standards
- Follow PEP 8 for Python code
- Use TypeScript with strict mode
- Write comprehensive unit tests (aim for 80%+ coverage)
- Implement proper error handling
- Include documentation for all public interfaces