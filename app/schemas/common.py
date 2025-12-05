from pydantic import BaseModel
from typing import Optional


class TaskDefinition(BaseModel):
    name: str
    description: Optional[str] = None


class ConditionDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    source_task: str
    outcome: str
    target_task_success: str
    target_task_failure: str
