from pydantic import BaseModel, Field
from typing import Any, Optional

class ResearchRequest(BaseModel):
    prompt: str = Field(
        ..., 
        min_length=5, 
        max_length=500, 
        description="The research topic or question you want the AI to investigate.",
        examples=["Who is the CEO of Tesla?", "Explain quantum computing in simple terms."]
    )

class ResearchResponse(BaseModel):
    message: str = Field(..., description="Confirmation message indicating the task has started.")
    task_id: str = Field(..., description="Unique identifier for the background task. Use this ID to check status.")

class TaskStatusResponse(BaseModel):
    state: str = Field(..., description="Current state of the task (e.g., PENDING, STARTED, SUCCESS, FAILURE).")
    result: Optional[Any] = Field(None, description="The result of the research task. Null if not yet completed.")
