# todo-app-api

this is a todo app api for practice with django.

## Features

- [x] Create a todo
- [x] List all todos
- [x] Update a todo
- [x] Delete a todo

## Schema

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

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/api/v1/tasks/` | List all tasks |
| POST | `/api/v1/tasks/` | Create a task |
| GET | `/api/v1/tasks/:id/` | Get a task |
| PUT | `/api/v1/tasks/:id/` | Update a task |
| DELETE | `/api/v1/tasks/:id/` | Delete a task |
