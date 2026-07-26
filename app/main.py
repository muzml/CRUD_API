from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.schemas import TaskCreate, TaskResponse
from app.database import tasks_db, find_task_by_id, get_next_id

# Initialize the FastAPI application instance
app = FastAPI(
    title="Task Management API",
    description="A lightweight REST API for managing tasks built with FastAPI.",
    version="1.0"
)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom exception handler to catch missing or invalid payload fields
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
    
    Returns a list of all tasks stored in memory.
    If no tasks exist, returns an empty list [].
    """
    return tasks_db


@app.get("/tasks/{id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_single_task(id: int):
    """
    Get Single Task Endpoint (GET /tasks/{id})
    
    - Accepts 'id' as a path parameter (integer).
    - Returns the task matching the specified 'id'.
    - If task is not found, returns HTTP 404 with {"error": "Task not found"}.
    """
    task = find_task_by_id(id)
    if not task:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )
    return task


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
