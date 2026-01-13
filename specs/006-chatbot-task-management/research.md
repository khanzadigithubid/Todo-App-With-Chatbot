# Research: AI Chatbot for Task Management

This document outlines the research and decisions made for the AI Chatbot feature.

## 1. OpenAI Agents SDK with FastAPI

**Decision**: We will use the standard OpenAI Python library and follow the official documentation for creating and running assistants.

**Rationale**: The `openai` library is well-documented and provides all the necessary functionality to create an assistant, add tools, and run conversations. The integration with FastAPI is straightforward, involving calling the OpenAI API from within a FastAPI route handler.

**Alternatives considered**: None, as using the official SDK is the most direct approach.

## 2. Context7 MCP Server for Tool Integration

**Decision**: The use of "Context7 MCP server" seems to be a project-specific or hypothetical tool. We will proceed by implementing the agent and tools directly within the FastAPI backend, following standard OpenAI SDK practices.

**Rationale**: There is no public information available for a "Context7 MCP server" related to OpenAI tool integration. The most direct and standard path is to define the tools as Python functions and pass them to the OpenAI assistant. This approach is well-documented and supported.

**Alternatives considered**: Searching for third-party tool integration frameworks, but this would add unnecessary complexity.

## 3. Urdu Language Support

**Decision**: Urdu language support will be implemented using `next-intl` on the frontend and by providing a system prompt to the AI agent to respond in Urdu.

**Rationale**: `next-intl` is already in use in the project for internationalization. We will add Urdu to the supported locales. For the chatbot, we can instruct the agent to respond in Urdu, which `gpt-4o` supports.

**Alternatives considered**: Using a separate translation API, but this would add latency and cost.

## 4. Voice Commands

**Decision**: Voice commands will be implemented on the frontend using the Web Speech API.

**Rationale**: The Web Speech API is a browser-standard API for speech recognition. It's relatively easy to implement and doesn't require any external libraries or services for basic use cases. The recognized text can then be sent to the chatbot API.

**Alternatives considered**: Using a third-party speech-to-text service, but this would add complexity and cost.

## 5. Conflict: Authentication

**Decision**: We will follow the feature specification and disable authentication for the `/api/chat` endpoint.

**Rationale**: The feature specification explicitly states to remove authentication for ease of testing during this phase. While the constitution mandates JWT authentication, a specific feature requirement can temporarily override a general principle for development and testing purposes. This deviation will be noted.
