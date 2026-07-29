from fastapi import FastAPI, status, Request, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.database import get_postgres_connection
from app.repository import PostgresTaskRepository
from app.service import TaskService
from app.auth_routes import router as auth_router
from app.user_routes import router as user_router
from app.dependencies import get_current_user


# Initialize the FastAPI application instance
app = FastAPI(
    title="Task Management API",
    description="A lightweight REST API for managing tasks built with FastAPI and PostgreSQL.",
    version="1.0"
)

# Include Routers (BE-05 Auth & User Routes)
app.include_router(auth_router)
app.include_router(user_router)




def get_task_service() -> TaskService:
    """
    Dependency Injection Provider Function.
    Instantiates PostgresTaskRepository and injects it into TaskService.
    """
    repository = PostgresTaskRepository(get_postgres_connection)
    return TaskService(repository)


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
    """
    return {
        "status": "ok"
    }


@app.get("/tasks", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def get_all_tasks(
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get All Tasks Endpoint (GET /tasks) - Protected
    Requires a valid Supabase JWT Bearer token.
    """
    return service.list_tasks()


@app.get("/tasks/{id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_single_task(
    id: int,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get Single Task Endpoint (GET /tasks/{id}) - Protected
    Requires a valid Supabase JWT Bearer token.
    """
    task = service.get_task(id)
    if task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )
    return task


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Create Task Endpoint (POST /tasks) - Protected
    Requires a valid Supabase JWT Bearer token.
    """
    return service.create_task(payload.title)


@app.put("/tasks/{id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    id: int,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Update Task Endpoint (PUT /tasks/{id}) - Protected
    Requires a valid Supabase JWT Bearer token.
    """
    if payload.title is None and payload.done is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid input: At least one field (title or done) must be provided"}
        )

    updated_task = service.update_task(id, payload.title, payload.done)
    if updated_task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )

    return updated_task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    id: int,
    service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete Task Endpoint (DELETE /tasks/{id}) - Protected
    Requires a valid Supabase JWT Bearer token.
    """
    success = service.delete_task(id)
    if not success:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

