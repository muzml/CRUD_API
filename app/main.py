from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.database import init_db, get_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI.
    Runs database initialization on startup.
    """
    init_db()
    yield


# Initialize the FastAPI application instance
app = FastAPI(
    title="Task Management API",
    description="A lightweight REST API for managing tasks built with FastAPI.",
    version="1.0",
    lifespan=lifespan
)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom exception handler to catch missing or empty payload fields
    and return HTTP 400 Bad Request instead of default HTTP 422.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid input: Title is required and cannot be empty"}
    )


@app.get("/")
def get_root():
    """
    Root Endpoint (GET /)
    
    Returns basic API metadata including API name, version, and supported endpoint paths.
    """
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def get_health():
    """
    Health Check Endpoint (GET /health)
    
    Used by monitoring tools or load balancers to verify if the server is alive and responding.
    """
    return {
        "status": "ok"
    }


@app.get("/tasks", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def get_all_tasks():
    """
    Get All Tasks Endpoint (GET /tasks)
    
    Fetches and returns a list of all tasks from SQLite database.
    If no tasks exist, returns an empty list [].
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks;")
    rows = cursor.fetchall()
    conn.close()
    
    tasks = [dict(row) for row in rows]
    return tasks


@app.get("/tasks/{id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_single_task(id: int):
    """
    Get Single Task Endpoint (GET /tasks/{id})
    
    - Accepts 'id' as a path parameter (integer).
    - Fetches the matching task from SQLite database.
    - If task is not found, returns HTTP 404 with {"error": "Task not found"}.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?;", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )
        
    return dict(row)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    """
    Create Task Endpoint (POST /tasks)
    
    - Accepts JSON body with 'title'.
    - Auto-generates a unique task ID (1, 2, 3...).
    - Sets default completion status 'done = False'.
    - Returns status HTTP 201 Created with the created task payload.
    """
    new_id = get_next_id()
    new_task = {
        "id": new_id,
        "title": payload.title,
        "done": False
    }
    tasks_db.append(new_task)
    return new_task


@app.put("/tasks/{id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(id: int, payload: TaskUpdate):
    """
    Update Task Endpoint (PUT /tasks/{id})
    
    - Updates title and/or done status of an existing task.
    - If task does not exist, returns HTTP 404 with {"error": "Task not found"}.
    - If no fields are provided in request body, returns HTTP 400 Bad Request.
    """
    task = find_task_by_id(id)
    if not task:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )
    
    if payload.title is None and payload.done is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid input: At least one field (title or done) must be provided"}
        )
    
    if payload.title is not None:
        task["title"] = payload.title
    
    if payload.done is not None:
        task["done"] = payload.done
        
    return task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    """
    Delete Task Endpoint (DELETE /tasks/{id})
    
    - Deletes task matching the specified 'id'.
    - Returns HTTP 204 No Content with empty response body.
    - If task does not exist, returns HTTP 404 with {"error": "Task not found"}.
    """
    task = find_task_by_id(id)
    if not task:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )
    
    tasks_db.remove(task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
