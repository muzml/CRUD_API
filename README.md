# 📝 Task Management REST API (FlyRank Week 3 Track)

A production-grade, containerized RESTful Task Management API built with **Python 3.11+**, **FastAPI**, **PostgreSQL 15**, and **Docker Compose** as part of the **FlyRank Backend Track (Week 3 Assignment A3: Containerize Your Stack)**.

---

## 🚀 Week 3 Assignment Evolution (Step-by-Step Transition)

This repository demonstrates the step-by-step evolution of a backend service across the three Week 3 assignments:

```
┌────────────────────────────────┐
│  Week 2 A1: In-Memory Storage  │  FastAPI base with Python list/dict state
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│  Week 3 A2: SQLite Persistence │  Relational storage with tasks.db & raw SQL
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐  Containerized PostgreSQL + Docker Volumes +
│  Week 3 A3: Containerized Stack│  3-Tier Layered Architecture (Routes → Service → Repo)
└────────────────────────────────┘
```

---

## 🛠️ Step-by-Step Implementation Stages (A3 Migration Log)

### 🔹 Stage 0 – Architecture Planning & Project Review
* **Goal**: Refactor monolithic SQL calls in route functions into a clean, decoupled 3-tier architecture.
* **Outcome**: Established contract: `Routes (main.py) → Service (service.py) → Repository (repository.py) → PostgreSQL (Docker)`. Request/response schemas (`schemas.py`) remained 100% unchanged.

### 🔹 Stage 1 – Docker & PostgreSQL Setup
* **Goal**: Containerize PostgreSQL using Docker and Docker Compose.
* **Files Created**: `docker-compose.yml`
* **Key Learning**: Used `postgres:15-alpine` for an ultra-lightweight footprint, mapped container port `5432:5432`, and configured a named Docker volume (`postgres_data`) for persistent disk storage.

### 🔹 Stage 2 – Environment Variables & Security
* **Goal**: Secure database credentials using environment variables (12-Factor App methodology).
* **Files Created/Modified**: `.env.example`, `.env`, `.gitignore`
* **Key Learning**: Hardcoding passwords breaks environment portability and creates security vulnerabilities. Created `.env.example` as a public template and added `.env` to `.gitignore`.

### 🔹 Stage 3 – Database Initialization (`init.sql`)
* **Goal**: Automate table creation and initial seed data insertion on container startup.
* **Files Created**: `init.sql`, updated `docker-compose.yml`
* **Key Learning**: Mounted `init.sql` into PostgreSQL's `/docker-entrypoint-initdb.d/` directory. PostgreSQL executes init scripts automatically on first container boot.

### 🔹 Stage 4 – PostgreSQL Repository & Service Layer
* **Goal**: Implement the Repository and Service patterns to isolate data access logic.
* **Files Created/Modified**: `app/repository.py`, `app/service.py`, `app/database.py`, `requirements.txt`
* **Key Learning**: Defined abstract `TaskRepository` interface and `PostgresTaskRepository` implementation using `psycopg2`. Utilized parameterized queries (`%s`) to prevent SQL injection and transaction commit/rollback logic.

### 🔹 Stage 5 – Connecting FastAPI via Dependency Injection
* **Goal**: Refactor FastAPI routes to use `TaskService` without modifying HTTP contracts.
* **Files Modified**: `app/main.py`
* **Key Learning**: Used FastAPI's `Depends(get_task_service)` for Dependency Injection. Route handlers no longer manage database connections or SQL queries.

### 🔹 Stage 6 – Persistence Testing & Volume Verification
* **Goal**: Verify data durability across database container restarts.
* **Outcome**: Executed `docker compose restart db` after inserting tasks via POST requests. Confirmed Docker volume `postgres_data` preserved all task rows intact.

### 🔹 Stage 7 – Documentation & GitHub Sync
* **Goal**: Document the complete architecture, setup instructions, and step-by-step progress.
* **Outcome**: Comprehensive `README.md` published and pushed stage-by-stage to GitHub.

---

## 🔐 Supabase Authentication Integration (BE-05 Auth Track)

### 🔹 Auth Stage 0 – Supabase Client & Config Setup
* **Goal**: Install Supabase SDK and set up client singleton module (`app/supabase_client.py`).

### 🔹 Auth Stage 1 – Signup & Login Endpoints
* **Goal**: Implement `POST /auth/signup` and `POST /auth/login` to authenticate users against Supabase Auth IdP.

### 🔹 Auth Stage 2 – Public & Protected Routes
* **Goal**: Implement `GET /public/info` (unauthenticated) and `GET /protected/profile` (token validation).

### 🔹 Auth Stage 3 – Centralized Auth Dependency & Task Endpoint Protection
* **Goal**: Create reusable `get_current_user` dependency with `HTTPBearer` scheme in `app/dependencies.py` and protect all `/tasks` CRUD endpoints.
* **Files Created/Modified**: `app/dependencies.py`, `app/main.py`, `app/user_routes.py`, `tests/test_stage3_auth.py`
* **Outcome**: All `/tasks` endpoints now mandate a valid Supabase JWT Bearer token in the `Authorization` header. Requests without valid tokens receive `401 Unauthorized`.

### 🔹 Auth Stage 4 – User-Scoped Tasks & Ownership Data Isolation (Multi-Tenancy)
* **Goal**: Bind tasks to authenticated user ID (`user_id`) in PostgreSQL database schema and repository queries for full multi-tenant data isolation.
* **Files Created/Modified**: `init.sql`, `app/schemas.py`, `app/repository.py`, `app/service.py`, `app/main.py`, `tests/test_stage4_user_scoped_tasks.py`
* **Outcome**: Users can only view, create, update, or delete their own tasks. Cross-user data access attempts return `404 Not Found`.

### 🔹 Auth Stage 5 – Session Management, Token Refresh & Logout Endpoints
* **Goal**: Complete authentication lifecycle with `POST /auth/refresh` and `POST /auth/logout` endpoints.
* **Files Created/Modified**: `app/schemas.py`, `app/auth_service.py`, `app/auth_routes.py`, `tests/test_stage5_auth_session.py`
* **Outcome**: Clients can seamlessly refresh access tokens using refresh tokens and terminate active sessions on demand.




## 🏗️ Architecture Overview

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
3. **Testability**: In automated test suites, `PostgresTaskRepository` can be easily swapped for an `InMemoryTaskRepository` without spinning up a live database.

---

## 💡 Why PostgreSQL Instead of SQLite?

| Feature | SQLite (Week 3 A2) | PostgreSQL (Week 3 A3 Standard) |
| :--- | :--- | :--- |
| **Architecture** | Serverless / File-based | Dedicated Client-Server RDBMS |
| **Concurrency** | Single-writer lock (limited concurrency) | Multi-Version Concurrency Control (MVCC) |
| **Containerization**| Local file binding | Isolated Docker service with volume persistence |
| **Data Types & Scaling**| Basic type affinities | Strict typing (`SERIAL`, `BOOLEAN`, JSONB, Indexing) |

---

## ⚙️ Environment Variables

Copy `.env.example` to create your local `.env` file:

```bash
cp .env.example .env
```

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `POSTGRES_USER` | `postgres` | Superuser username for PostgreSQL |
| `POSTGRES_PASSWORD` | `postgrespassword` | Password for PostgreSQL authentication |
| `POSTGRES_DB` | `taskdb` | Target database name |
| `POSTGRES_HOST` | `localhost` | Database server host |
| `POSTGRES_PORT` | `5432` | Database server port |
| `DATABASE_URL` | `postgresql://postgres:postgrespassword@localhost:5432/taskdb` | Standard connection URI |

---

## 🐳 Docker Setup & Running Instructions

### 1. Start PostgreSQL Container
```bash
docker compose up -d
```

### 2. Install Dependencies & Run Server
```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The API will start at **`http://127.0.0.1:8000`**.

---

## 📖 API Endpoints Overview

Interactive Swagger UI documentation is available at:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

| HTTP Method | Endpoint | Description | Auth Required | Expected Status |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | API Metadata & Entrypoint | ❌ Public | `200 OK` |
| `GET` | `/health` | Operational Health Check | ❌ Public | `200 OK` |
| `GET` | `/public/info` | Public API Status Info | ❌ Public | `200 OK` |
| `POST` | `/auth/signup` | Register new user in Supabase Auth | ❌ Public | `201 Created` / `400` |
| `POST` | `/auth/login` | Authenticate user & return JWT tokens | ❌ Public | `200 OK` / `400` |
| `POST` | `/auth/refresh` | Exchange refresh token for new JWT session | ❌ Public | `200 OK` / `400` |
| `POST` | `/auth/logout` | Terminate active user session | 🔒 Bearer JWT | `200 OK` / `401` |
| `GET` | `/protected/profile` | Retrieve user profile from Supabase JWT | 🔒 Bearer JWT | `200 OK` / `401` |
| `GET` | `/tasks` | Retrieve all user-scoped tasks | 🔒 Bearer JWT | `200 OK` / `401` |
| `GET` | `/tasks/{id}` | Retrieve single user-scoped task by `id` | 🔒 Bearer JWT | `200 OK` / `401` / `404` |
| `POST` | `/tasks` | Create a new user-scoped task | 🔒 Bearer JWT | `201 Created` / `400` / `401` |
| `PUT` | `/tasks/{id}` | Update task title and/or `done` status | 🔒 Bearer JWT | `200 OK` / `400` / `401` / `404` |
| `DELETE` | `/tasks/{id}` | Delete task by `id` | 🔒 Bearer JWT | `204 No Content` / `401` / `404` |



---

## 📌 Track Info

Built for **FlyRank Backend Track Week 3 Assignments (A1, A2, & A3: Containerize Your Stack)**.
