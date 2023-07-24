# todo-app-api

this is a todo app api for practice with django.

## Features

- [x] Create a user
- [x] List all users
- [x] Get a user
- [x] Update a user
- [x] Delete a user
- [x] Create a todo
- [x] List all todos
- [x] Get a todo
- [x] Update a todo
- [x] Delete a todo

## Schema

### User

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int | Unique identifier |
| username | string | Username of the user |
| password | string | Password of the user |

### Task

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | int | Unique identifier |
| title | string | Title of the task |
| description | string | Description of the task |
| completed | boolean | Status of the task |
| created_at | datetime | Date of creation |
| updated_at | datetime | Date of last update |
| author | string | Author of the task |

## Endpoints

### User

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/api/v1/users/` | List all users |
| POST | `/api/v1/users/` | Create a user |
| GET | `/api/v1/users/:id/` | Get a user |
| PUT | `/api/v1/users/:id/` | Update a user |
| DELETE | `/api/v1/users/:id/` | Delete a user |

### Task

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/api/v1/tasks/` | List all tasks |
| POST | `/api/v1/tasks/` | Create a task |
| GET | `/api/v1/tasks/:id/` | Get a task |
| PUT | `/api/v1/tasks/:id/` | Update a task |
| DELETE | `/api/v1/tasks/:id/` | Delete a task |
