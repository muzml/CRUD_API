# 📝 Task Management REST API

A clean, beginner-friendly RESTful Task Management API built with **Python 3.10+** and **FastAPI** as part of the **FlyRank Backend Track (Week 2)** assignment.

This project implements full CRUD (Create, Read, Update, Delete) operations using an **in-memory Python data store** without external databases, strictly adhering to REST principles and proper HTTP status codes.

---

## 🚀 Features

- **Root & Health Check**: API discovery endpoint (`GET /`) and operational status check (`GET /health`).
- **Full CRUD Operations**:
  - `GET /tasks`: List all tasks.
  - `GET /tasks/{id}`: Fetch a specific task by ID.
  - `POST /tasks`: Create a new task with auto-generated ID (`done=False`).
  - `PUT /tasks/{id}`: Update task title and/or completion status.
  - `DELETE /tasks/{id}`: Delete a task (`204 No Content`).
- **Strict Input Validation**: Rejects empty or missing title payloads with `400 Bad Request`.
- **Interactive Documentation**: Built-in Swagger UI available at `/docs` and ReDoc at `/redoc`.

---

## 🛠️ Technology Stack

- **Language**: Python 3.10+
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)

---

## 📁 Project Structure

```text
Crud_API/
├── app/
│   ├── __init__.py      # Package marker
│   ├── main.py          # FastAPI application initialization & endpoint handlers
│   ├── schemas.py       # Pydantic data models & custom validators
│   └── database.py      # In-memory storage list & auto-increment ID logic
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python package dependencies
└── README.md            # Project documentation
```

---

## ⚡ Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/muzml/CRUD_API.git
cd CRUD_API
```

### 2. Create and Activate Virtual Environment (Optional but Recommended)
**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Run the API Server
```bash
python -m uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

---

## 📖 API Documentation & Endpoints

Interactive Swagger UI documentation is available at:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

### Summary of Available Endpoints

| HTTP Method | Endpoint | Description | Expected Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API Metadata & Entrypoint | `200 OK` |
| `GET` | `/health` | Server Health Status | `200 OK` |
| `GET` | `/tasks` | Get all tasks | `200 OK` |
| `GET` | `/tasks/{id}` | Get single task by ID | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Create a new task | `201 Created` / `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update title and/or status | `200 OK` / `400 Bad Request` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete task by ID | `204 No Content` / `404 Not Found` |

---

## 🧪 cURL Request & Response Examples

### 1. Get API Information (`GET /`)
```bash
curl -X GET "http://127.0.0.1:8000/"
```
**Response (`200 OK`):**
```json
{
  "name": "Task API",
  "version": "1.0",
  "endpoints": ["/tasks"]
}
```

---

### 2. Health Check (`GET /health`)
```bash
curl -X GET "http://127.0.0.1:8000/health"
```
**Response (`200 OK`):**
```json
{
  "status": "ok"
}
```

---

### 3. Create a New Task (`POST /tasks`)
```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Buy milk"}'
```
**Response (`201 Created`):**
```json
{
  "id": 1,
  "title": "Buy milk",
  "done": false
}
```

**Invalid Input Error (`400 Bad Request`):**
```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "   "}'
```
```json
{
  "error": "Invalid input: Title is required and cannot be empty"
}
```

---

### 4. Fetch All Tasks (`GET /tasks`)
```bash
curl -X GET "http://127.0.0.1:8000/tasks"
```
**Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "title": "Buy milk",
    "done": false
  }
]
```

---

### 5. Fetch Single Task (`GET /tasks/1`)
```bash
curl -X GET "http://127.0.0.1:8000/tasks/1"
```
**Response (`200 OK`):**
```json
{
  "id": 1,
  "title": "Buy milk",
  "done": false
}
```

**Not Found Error (`404 Not Found`):**
```json
{
  "error": "Task not found"
}
```

---

### 6. Update Task (`PUT /tasks/1`)
```bash
curl -X PUT "http://127.0.0.1:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "Buy organic almond milk", "done": true}'
```
**Response (`200 OK`):**
```json
{
  "id": 1,
  "title": "Buy organic almond milk",
  "done": true
}
```

---

### 7. Delete Task (`DELETE /tasks/1`)
```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```
**Response (`204 No Content`):** Empty Body

---

## 📌 License & Track Info

Built for **FlyRank Backend Track Week 2 Assignment**.
