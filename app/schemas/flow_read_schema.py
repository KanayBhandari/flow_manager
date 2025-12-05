from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class TaskRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_name: str
    success: bool
    output: dict
    timestamp: datetime

class FlowRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    flow_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime]
    tasks: Optional[List[TaskRunResponse]] = None

class FlowDefinitionResponse(BaseModel):
    id: str
    name: str
    definition: dict

    class Config:
        orm_mode = True
