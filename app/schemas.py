from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.
    
    The client only needs to provide the 'title'.
    The backend will automatically generate 'id' and set 'done = false'.
    """
    title: str = Field(..., description="The title of the task", example="Buy milk")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value: str) -> str:
        """
        Custom validator to ensure title is not empty or just whitespace.
        """
        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("Task title cannot be empty or contain only whitespace.")
        return stripped_value


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task (PUT /tasks/{id}).
    
    Both fields are optional so the client can update title, done status, or both.
    """
    title: Optional[str] = Field(None, description="Updated task title", example="Buy organic milk")
    done: Optional[bool] = Field(None, description="Updated completion status", example=True)

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value: Optional[str]) -> Optional[str]:
        """
        Ensure that if title is provided in an update payload, it is not empty.
        """
        if value is not None:
            stripped_value = value.strip()
            if not stripped_value:
                raise ValueError("Task title cannot be empty or contain only whitespace.")
            return stripped_value
        return value


class TaskResponse(BaseModel):
    """
    Schema for outgoing task responses.
    
    Represents the full Task object sent back to clients.
    """
    id: int = Field(..., description="Unique task identifier", example=1)
    title: str = Field(..., description="Task title", example="Buy milk")
    done: bool = Field(..., description="Task completion status", example=False)


# ==========================================
# Authentication Schemas (BE-05 Auth)
# ==========================================

class AuthCredentials(BaseModel):
    """
    Schema for signup and login requests.
    """
    email: str = Field(..., description="User email address", example="user@example.com")
    password: str = Field(..., description="User password (min 6 characters)", example="secret123")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        if not value or "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value


class AuthResponse(BaseModel):
    """
    Schema for authentication response containing JWT tokens.
    """
    access_token: str = Field(..., description="Short-lived JWT Access Token")
    refresh_token: Optional[str] = Field(None, description="Refresh Token for obtaining new access tokens")
    token_type: str = Field("bearer", description="Token type")
    expires_in: Optional[int] = Field(None, description="Expiration time in seconds")
    user_id: str = Field(..., description="Unique Supabase User UUID")
    email: str = Field(..., description="User email address")

