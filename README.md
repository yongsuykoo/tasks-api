# Tasks API 🚀

A complete REST API for managing tasks built with FastAPI + SQLite.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Pydantic models for validation
- ✅ Auto-generated OpenAPI docs at `/docs`
- ✅ Filtering by completion status and priority
- ✅ Proper HTTP status codes and error handling
- ✅ CORS enabled for frontend integration

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API welcome & info |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get task by ID |
| POST | `/tasks` | Create new task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/health` | Health check |

## Query Parameters

- `skip` - Pagination offset (default: 0)
- `limit` - Max results (default: 100)
- `completed` - Filter by completion status (true/false)
- `priority` - Filter by priority (low/medium/high)

## Task Schema

```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (default: false)",
  "priority": "low | medium | high (default: medium)"
}
```

## Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Built with ❤️ by Yongskie 🇵🇭
