from fastapi import FastAPI

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
