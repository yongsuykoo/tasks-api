# Tasks API 🚀

A complete REST API for managing tasks built with FastAPI + SQLite.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Pydantic models for validation
- ✅ Auto-generated OpenAPI docs at `/docs`
- ✅ Filtering by status and priority
- ✅ Proper HTTP status codes & error handling
- ✅ CORS enabled

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get task by ID |
| POST | `/tasks` | Create new task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| DELETE | `/tasks` | Delete completed tasks |

## Query Parameters

- `skip` - Pagination offset (default: 0)
- `limit` - Max results (default: 100)
- `completed` - Filter by status (true/false)
- `priority` - Filter by priority (low/medium/high)

## Task Schema

```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": false,
  "priority": "low | medium | high"
}
```

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Author

Built with ❤️ by Yongskie from Philippines 🇵🇭
