from pydantic import BaseModel

from typing import (
    Any,
    Optional
)


class TaskResult(BaseModel):
    id: str
    status: str
    error: Optional[str] = None
    result: Optional[Any] = None
