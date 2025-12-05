from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime

from app.db.models import FlowDefinition, FlowRun, TaskRun
from app.core.logger import logger


# FlowDefinition storage / retrieval
def create_or_update_flow_definition(db: Session, flow_id: str, name: str, definition: Dict[str, Any]) -> FlowDefinition:
    existing = db.query(FlowDefinition).filter(FlowDefinition.id == flow_id).one_or_none()
    if existing:
        existing.name = name
        existing.definition = definition
        db.add(existing)
        db.commit()
        db.refresh(existing)
        logger.debug("Updated FlowDefinition %s", flow_id)
        return existing

    flow_def = FlowDefinition(id=flow_id, name=name, definition=definition)
    db.add(flow_def)
    db.commit()
    db.refresh(flow_def)
    logger.debug("Created FlowDefinition %s", flow_id)
    return flow_def


def get_flow_definition(db: Session, flow_id: str) -> Optional[FlowDefinition]:
    return db.query(FlowDefinition).filter(FlowDefinition.id == flow_id).one_or_none()


# FlowRun lifecycle
def create_flow_run(db: Session, flow_id: str, status: str = "running") -> FlowRun:
    fr = FlowRun(flow_id=flow_id, status=status, start_time=datetime.utcnow())
    db.add(fr)
    db.commit()
    db.refresh(fr)
    logger.debug("Created FlowRun id=%s for flow=%s", fr.id, flow_id)
    return fr


def update_flow_run_status(db: Session, flow_run: FlowRun, status: str) -> FlowRun:
    flow_run.status = status
    if status in ("completed", "failed"):
        flow_run.end_time = datetime.utcnow()
    db.add(flow_run)
    db.commit()
    db.refresh(flow_run)
    logger.debug("Updated FlowRun id=%s status=%s", flow_run.id, status)
    return flow_run


# TaskRun creation
def create_task_run(db: Session, flow_run_id: int, task_name: str, success: bool, output: dict) -> TaskRun:
    tr = TaskRun(
        flow_run_id=flow_run_id,
        task_name=task_name,
        success=success,
        output=output
    )
    db.add(tr)
    db.commit()
    db.refresh(tr)
    logger.debug("Created TaskRun id=%s task=%s success=%s", tr.id, task_name, success)
    return tr

# -------------------------
# Flow Definitions
# -------------------------

def get_all_flow_definitions(db: Session):
    return db.query(FlowDefinition).all()


def get_flow_definition_by_id(db: Session, flow_id: str):
    return db.query(FlowDefinition).filter(FlowDefinition.id == flow_id).first()

# -------------------------
# Flow Runs
# -------------------------

def get_all_flow_runs(db: Session):
    return db.query(FlowRun).all()


def get_flow_runs_by_flow_id(db: Session, flow_id: str):
    return db.query(FlowRun).filter(FlowRun.flow_id == flow_id).all()


def get_flow_run_by_id(db: Session, run_id: int):
    return db.query(FlowRun).filter(FlowRun.id == run_id).first()


# -------------------------
# Task Runs
# -------------------------

def get_task_runs_by_flow_run_id(db: Session, flow_run_id: int):
    return db.query(TaskRun).filter(TaskRun.flow_run_id == flow_run_id).all()


def get_task_run_by_id(db: Session, task_run_id: int):
    return db.query(TaskRun).filter(TaskRun.id == task_run_id).first()
