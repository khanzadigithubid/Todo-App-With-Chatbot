# Data Model: AI Chatbot for Task Management

This feature does not introduce any new data models. It utilizes the existing `User` and `Task` models defined in the previous phases.

The chatbot interacts with the existing `tasks` table in the database, which is mapped to the `Task` SQLModel. The `user_id` for all operations will be hardcoded to `"testuser"` for this phase.
