# 📝 Task Management REST API (Containerized PostgreSQL & Clean Architecture)

A production-grade, containerized RESTful Task Management API built with **Python 3.11+**, **FastAPI**, **PostgreSQL 15**, and **Docker Compose** as part of the **FlyRank Backend Track (Week 3 Assignment A3: Containerize Your Stack)**.

This project refactors the SQLite CRUD API into a **3-tier Layered Architecture (Routes → Service → Repository → PostgreSQL)** running inside a containerized environment with persistent Docker volumes.

---

## 🏗️ Architecture Overview

The application strictly separates HTTP concerns, business logic, and database access:

```
                  ┌─────────────────────────────────────────┐
                  │          HTTP Request (Client)          │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │       Routes Layer (app/main.py)        │
                  │   Handles HTTP parsing & JSON responses │
                  └────────────────────┬────────────────────┘
                                       │ (Depends / DI)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │      Service Layer (app/service.py)     │
                  │   Business logic & application rules    │
                  └────────────────────┬────────────────────┘
                                       │ (TaskRepository ABC)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │   Repository (app/repository.py)       │
                  │   PostgresTaskRepository (psycopg2)     │
                  └────────────────────┬────────────────────┘
                                       │ (TCP Port 5432)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │   PostgreSQL Database (Docker)          │
                  │   Container: task_postgres_db           │
                  └─────────────────────────────────────────┘
```

---

## 🏛️ Why Repository Pattern & Clean Architecture?

1. **Decoupled Business Logic**: The Service and Route layers depend on an abstract `TaskRepository` interface. They have zero knowledge of database driver specifics.
2. **Seamless Database Swapping**: Changing from SQLite to PostgreSQL required **zero changes** to route endpoints or request/response schemas.
3. **Testability**: In automated test suites, the `PostgresTaskRepository` can be easily swapped for an `InMemoryTaskRepository` without spinning up a live database.

---

## 💡 Why PostgreSQL Instead of SQLite?

| Feature | SQLite | PostgreSQL (Production Standard) |
| :--- | :--- | :--- |
| **Architecture** | Serverless / File-based | Dedicated Client-Server RDBMS |
| **Concurrency** | Single-writer lock (limited concurrency) | Multi-Version Concurrency Control (MVCC) |
| **Containerization**| Local file binding | Isolated Docker service with volume persistence |
| **Data Types & Scaling**| Basic type affinities | Strict typing (`SERIAL`, `BOOLEAN`, JSONB, Indexing) |

---

## ⚙️ Environment Variables

Configuration is loaded from environment variables using `python-dotenv`.

Copy `.env.example` to create your local `.env` file:

```bash
cp .env.example .env
```

### Configuration Keys

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `POSTGRES_USER` | `postgres` | Superuser username for PostgreSQL |
| `POSTGRES_PASSWORD` | `postgrespassword` | Password for PostgreSQL authentication |
| `POSTGRES_DB` | `taskdb` | Target database name |
| `POSTGRES_HOST` | `localhost` | Database server host |
| `POSTGRES_PORT` | `5432` | Database server port |
| `DATABASE_URL` | `postgresql://postgres:postgrespassword@localhost:5432/taskdb` | Standard connection URI |

> ⚠️ **Security Note**: `.env` contains local environment secrets and is ignored by Git via `.gitignore`. Never commit `.env` files to public source control.

---

## 🐳 Docker & Containerization Setup

The PostgreSQL stack is containerized using `postgres:15-alpine` and managed via `docker-compose.yml`.

### Key Features:
* **Alpine Linux Base**: Ultra-lightweight Docker image (~5MB footprint).
* **Automatic Initialization**: Mounts `init.sql` into `/docker-entrypoint-initdb.d/init.sql` to auto-create tables and seed initial data on first launch.
* **Data Persistence**: Uses a named Docker volume (`postgres_data:/var/lib/postgresql/data`) to preserve database rows across container restarts.

---

## 🚀 Quick Start & Running Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/muzml/CRUD_API.git
cd CRUD_API
```

### 2. Start PostgreSQL Container
```bash
docker compose up -d
```

Verify container status:
```bash
docker compose ps
```

### 3. Set Up Python Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source .venv/bin/activate

# Install requirements
python -m pip install -r requirements.txt
```

### 4. Run FastAPI Application
```bash
python -m uvicorn app.main:app --reload
```

The API will start at **`http://127.0.0.1:8000`**.

---

## 📖 API Endpoints Overview

Interactive Swagger UI documentation is available at:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

| HTTP Method | Endpoint | Description | Expected Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API Metadata & Entrypoint | `200 OK` |
| `GET` | `/health` | Operational Health Check | `200 OK` |
| `GET` | `/tasks` | Retrieve all tasks from PostgreSQL | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve single task by integer `id` | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Create a new task (`done` defaults to `false`) | `201 Created` / `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update task title and/or `done` status | `200 OK` / `400` / `404` |
| `DELETE` | `/tasks/{id}` | Delete task by `id` | `204 No Content` / `404 Not Found` |

---

## 🧪 Data Persistence Verification

To verify that Docker volumes preserve database state across restarts:

1. **Create a new task via POST request**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/tasks" \
        -H "Content-Type: application/json" \
        -d '{"title": "Verify Docker Volume Persistence"}'
   ```
2. **Restart the PostgreSQL database container**:
   ```bash
   docker compose restart db
   ```
3. **Fetch all tasks**:
   ```bash
   curl -X GET "http://127.0.0.1:8000/tasks"
   ```
4. **Result**: The newly created task persists safely!

---

## 📌 Track Info & Credits

Built as part of **FlyRank Backend Track Week 3 Assignment A3: Containerize Your Stack**.
