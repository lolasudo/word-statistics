from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskStatus(BaseModel):
    status: str
    progress: Optional[int] = None
    message: Optional[str] = None
    error: Optional[str] = None
    download_url: Optional[str] = None