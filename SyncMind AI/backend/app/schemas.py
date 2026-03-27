from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel


class WorkspaceCreate(BaseModel):
    name: str


class WorkspaceOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    workspace_id: int


class ProjectOut(BaseModel):
    id: int
    name: str
    workspace_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TranscriptCreate(BaseModel):
    project_id: int
    raw_text: str


class TranscriptOut(BaseModel):
    id: int
    project_id: int
    raw_text: str
    created_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    owner: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = "pending"


class TaskCreate(TaskBase):
    project_id: int
    source_transcript_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    owner: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class TaskOut(TaskBase):
    id: int
    project_id: int
    source_transcript_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ActionItemsResponse(BaseModel):
    tasks: List[TaskOut]

