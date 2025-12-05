from pydantic import BaseModel
from typing import List
from app.schemas.common import TaskDefinition, ConditionDefinition


class FlowDefinitionSchema(BaseModel):
    id: str
    name: str
    start_task: str
    tasks: List[TaskDefinition]
    conditions: List[ConditionDefinition]


class FlowRequest(BaseModel):
    flow: FlowDefinitionSchema
