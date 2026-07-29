# 📝 Task Management REST API (FlyRank Backend Track)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)
![Docker](https://img.shields.io/badge/Docker%20Compose-2.0+-2496ED.svg)
![Supabase](https://img.shields.io/badge/Supabase-Auth%20IdP-3ECF8E.svg)
![Tests](https://img.shields.io/badge/Tests-21%2F21%20Passing-brightgreen.svg)

A production-grade, containerized RESTful Task Management API built with **Python 3.11+**, **FastAPI**, **PostgreSQL 15**, **Docker Compose**, and **Supabase Auth** as part of the **FlyRank Backend Track**.

---

## 🚀 Week 3 & BE-05 Evolution (Step-by-Step Transition)

This repository demonstrates the step-by-step evolution of a production backend service:

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
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐  Supabase Auth IdP + JWT Bearer Dependencies +
│  BE-05: Auth & Multi-Tenancy   │  User-Scoped Task Ownership & Session Management
└────────────────────────────────┘
```

---

## 🛠️ Implementation Stages Log

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

---

## 🔐 Supabase Authentication Integration (BE-05 Auth Track)

### 🔹 Auth Stage 0 – Supabase Client & Config Setup
* **Goal**: Install Supabase SDK and set up singleton client module (`app/supabase_client.py`).

### 🔹 Auth Stage 1 – Signup & Login Endpoints
* **Goal**: Implement `POST /auth/signup` and `POST /auth/login` to authenticate users against Supabase Auth IdP.

### 🔹 Auth Stage 2 – Public & Protected Routes
* **Goal**: Implement `GET /public/info` (unauthenticated) and `GET /protected/profile` (token validation).

### 🔹 Auth Stage 3 – Centralized Auth Dependency & Task Protection
* **Goal**: Create reusable `get_current_user` dependency with `HTTPBearer` scheme in `app/dependencies.py` and protect all `/tasks` CRUD endpoints.
* **Outcome**: All `/tasks` endpoints now mandate a valid Supabase JWT Bearer token in the `Authorization` header. Requests without valid tokens receive `401 Unauthorized`.

### 🔹 Auth Stage 4 – User-Scoped Tasks & Ownership Data Isolation
* **Goal**: Bind tasks to authenticated user ID (`user_id`) in PostgreSQL database schema and repository queries for full multi-tenant data isolation.
* **Outcome**: Users can only view, create, update, or delete their own tasks. Cross-user data access attempts return `404 Not Found`.

### 🔹 Auth Stage 5 – Session Management, Token Refresh & Logout
* **Goal**: Complete authentication lifecycle with `POST /auth/refresh` and `POST /auth/logout` endpoints.
* **Outcome**: Clients can seamlessly refresh access tokens using refresh tokens and terminate active sessions on demand.

### 🔹 Auth Stage 6 – Master Test Suite & OpenAPI Security Configuration
* **Goal**: Configure OpenAPI Bearer security scheme in `app/main.py` for Swagger UI (`/docs`) and build master test runner `tests/run_all_tests.py`.
* **Outcome**: Master test suite passing with 100% assertions across all authentication stages. Interactive Swagger documentation fully configured for JWT authorization.

---

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
                   └───────────┬──────────────────┬──────────┘
                               │                  │
               (Depends / DI)  ▼                  ▼  (JWT Validation)
       ┌───────────────────────────────┐  ┌───────────────────────────────┐
       │ Service Layer (app/service.py)│  │ Supabase Auth (dependencies)  │
       │ Application Business Rules    │  │ get_current_user (HTTPBearer) │
       └───────────────┬───────────────┘  └───────────────────────────────┘
                       │ (TaskRepository ABC)
                       ▼
       ┌───────────────────────────────┐
       │ Repository (app/repository.py)│
       │ PostgresTaskRepository        │
       └───────────────┬───────────────┘
                       │ (TCP Port 5432)
                       ▼
       ┌───────────────────────────────┐
       │ PostgreSQL Database (Docker)  │
       │ Table: tasks (with user_id)   │
       └───────────────────────────────┘
```

---

## 📁 Directory Structure

```text
Crud_API/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI Application Entrypoint & OpenAPI config
│   ├── schemas.py           # Pydantic Request/Response DTO Schemas
│   ├── database.py          # PostgreSQL connection provider
│   ├── repository.py        # TaskRepository ABC, PostgresTaskRepository & SQLite
│   ├── service.py           # TaskService business logic layer
│   ├── dependencies.py      # get_current_user Auth Dependency (HTTPBearer)
│   ├── supabase_client.py   # Supabase client singleton initialization
│   ├── auth_service.py      # AuthService interacting with Supabase Auth IdP
│   ├── auth_routes.py       # Authentication routes (/auth/signup, /login, /refresh, /logout)
│   └── user_routes.py       # Public & Protected profile routes (/public/info, /protected/profile)
├── tests/
│   ├── __init__.py
│   ├── test_stage3_auth.py  # Stage 3 Auth dependency & route protection tests
│   ├── test_stage4_user_scoped_tasks.py  # Stage 4 Multi-tenant data isolation tests
│   ├── test_stage5_auth_session.py        # Stage 5 Token refresh & logout tests
│   └── run_all_tests.py    # Master Test Runner executing full suite
├── docker-compose.yml       # Docker Compose setup for PostgreSQL 15 Alpine
├── init.sql                 # Automated database initialization & seeding script
├── requirements.txt         # Python dependencies
├── .env.example             # Environment configuration template
└── README.md                # Comprehensive documentation
```

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
| `SUPABASE_URL` | `https://your-project-id.supabase.co` | Supabase Project API URL |
| `SUPABASE_KEY` | `your-supabase-anon-key` | Supabase Anon Public API Key |

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

## 🧪 Running Automated Tests

Run the master test runner script to execute all unit and integration test suites:

```bash
python tests/run_all_tests.py
```

### Expected Output:
```text
======================================================================
 [RUNNING FULL SUITE] (STAGES 3, 4, 5) - AUTHENTICATION & TASK API
======================================================================

--- [STAGE 3] Centralized Auth Dependency & Endpoint Protection ---
[PASS] Test 1: GET /public/info is publicly accessible (200 OK)
[PASS] Test 2: GET /protected/profile without token returns 401 Unauthorized
[PASS] Test 3: GET /tasks without token returns 401 Unauthorized
[PASS] Test 4: GET /tasks/1 without token returns 401 Unauthorized
[PASS] Test 5: POST /tasks without token returns 401 Unauthorized
[PASS] Test 6: PUT /tasks/1 without token returns 401 Unauthorized
[PASS] Test 7: DELETE /tasks/1 without token returns 401 Unauthorized
[PASS] Test 8: GET /protected/profile with authorized token returns 200 OK & user data

--- [STAGE 4] User-Scoped Tasks & Ownership Data Isolation ---
[PASS] Test 1: User A created Task 1 (user_id=user-aaa-111)
[PASS] Test 2: User B created Task 2 (user_id=user-bbb-222)
[PASS] Test 3: User A list endpoint returns ONLY User A tasks
[PASS] Test 4: User B requesting GET /tasks/{User A Task ID} receives 404 Not Found
[PASS] Test 5: User B requesting PUT /tasks/{User A Task ID} receives 404 Not Found
[PASS] Test 6: User B requesting DELETE /tasks/{User A Task ID} receives 404 Not Found
[PASS] Test 7: User A can successfully update own task
[PASS] Test 8: User A can successfully delete own task

--- [STAGE 5] Session Management, Token Refresh & Logout ---
[PASS] Test 1: POST /auth/refresh with empty token returns 400 Bad Request
[PASS] Test 2: POST /auth/refresh with invalid token returns 400 Bad Request
[PASS] Test 3: POST /auth/logout without token returns 401 Unauthorized
[PASS] Test 4: POST /auth/logout with valid token returns 200 OK & logout message
[PASS] Test 5: POST /auth/refresh with valid token returns new AuthResponse

======================================================================
 [SUCCESS] ALL TEST ASSERTIONS PASSED WITH 100% COVERAGE!
======================================================================
```

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

Built for **FlyRank Backend Track (Week 3 Assignments A1, A2, A3 & BE-05 Supabase Auth Integration)**.
