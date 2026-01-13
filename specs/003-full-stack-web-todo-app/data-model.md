# Data Model: Full-Stack Web Todo App

The database will consist of two main tables: `users` and `tasks`.

## `users` Table

| Column      | Type          | Constraints              | Description                  |
|-------------|---------------|--------------------------|------------------------------|
| `id`        | `string`      | **Primary Key**          | Unique identifier for the user |
| `email`     | `string`      | **Unique**, **Not Null** | User's email address         |
| `name`      | `string`      | Not Null                 | User's name                  |
| `created_at`| `datetime`    | Default: `NOW()`         | Timestamp of user creation   |

## `tasks` Table

| Column        | Type          | Constraints                      | Description                           |
|---------------|---------------|----------------------------------|---------------------------------------|
| `id`          | `integer`     | **Primary Key**, Auto-increment  | Unique identifier for the task        |
| `user_id`     | `string`      | **Foreign Key** (-> `users.id`)  | Associates the task with a user       |
| `title`       | `string`      | **Not Null**                     | The title of the task                 |
| `description` | `text`        | Nullable                         | A detailed description of the task    |
| `completed`   | `boolean`     | Default: `false`                 | The completion status of the task     |
| `created_at`  | `datetime`    | Default: `NOW()`                 | Timestamp of task creation            |
| `updated_at`  | `datetime`    | Default: `NOW()`, On Update: `NOW()` | Timestamp of the last task update     |

**Indexes**:
- An index will be created on `tasks.user_id` to optimize queries for a user's tasks.
- An index will be created on `tasks.completed` to optimize filtering by completion status.
