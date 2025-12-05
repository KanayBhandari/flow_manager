from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import repositories as repo
from app.schemas.flow_read_schema import (
    FlowDefinitionResponse,
    FlowRunResponse,
    TaskRunResponse
)

router = APIRouter(prefix="/flows", tags=["Flow Reads"])


# ---------------------------------------
# Flow Definitions
# ---------------------------------------

@router.get("/", response_model=list[FlowDefinitionResponse])
def list_flows(db: Session = Depends(get_db)):
    return repo.get_all_flow_definitions(db)

# ---------------------------------------
# Flow Runs
# ---------------------------------------

@router.get("/runs", response_model=list[FlowRunResponse])
def list_flow_runs(db: Session = Depends(get_db)):
    return repo.get_all_flow_runs(db)


@router.get("/{flow_id}/runs", response_model=list[FlowRunResponse])
def get_runs_for_flow(flow_id: str, db: Session = Depends(get_db)):
    return repo.get_flow_runs_by_flow_id(db, flow_id)


@router.get("/runs/{run_id}", response_model=FlowRunResponse)
def get_flow_run(run_id: int, db: Session = Depends(get_db)):
    flow_run = repo.get_flow_run_by_id(db, run_id)
    if not flow_run:
        raise HTTPException(status_code=404, detail="Flow run not found")

    # Fetch related tasks
    task_runs = repo.get_task_runs_by_flow_run_id(db, run_id)
    flow_run.tasks = task_runs  # Attach tasks to ORM object

    # Let Pydantic handle ORM → response conversion
    return FlowRunResponse.model_validate(flow_run, from_attributes=True)



# ---------------------------------------
# Task Runs
# ---------------------------------------

@router.get("/task-runs/{task_run_id}", response_model=TaskRunResponse)
def get_task_run(task_run_id: int, db: Session = Depends(get_db)):
    task_run = repo.get_task_run_by_id(db, task_run_id)
    if not task_run:
        raise HTTPException(status_code=404, detail="Task run not found")
    return task_run

@router.get("/{flow_id}", response_model=FlowDefinitionResponse)
def get_flow(flow_id: str, db: Session = Depends(get_db)):
    flow = repo.get_flow_definition_by_id(db, flow_id)
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    return flow

