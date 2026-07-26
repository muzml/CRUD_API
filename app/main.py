from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.schemas import TaskResponse
from app.database import tasks_db, find_task_by_id

# Initialize the FastAPI application instance
app = FastAPI(
    title="Task Management API",
    description="A lightweight REST API for managing tasks built with FastAPI.",
    version="1.0"
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
