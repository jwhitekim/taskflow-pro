from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_serializer

from models import TaskStatus


def to_utc_iso8601(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    else:
        value = value.astimezone(timezone.utc)
    return value.isoformat().replace("+00:00", "Z")


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    due_at: Optional[datetime] = None


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = None
    status: TaskStatus
    due_at: Optional[datetime] = None


class TaskListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: TaskStatus
    due_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    @field_serializer("due_at", "created_at", "updated_at")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        return to_utc_iso8601(value)


class TaskDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    due_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    @field_serializer("due_at", "created_at", "updated_at")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        return to_utc_iso8601(value)
