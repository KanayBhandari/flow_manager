from typing import Dict
from datetime import datetime

from app.core.logger import logger
from app.flows.task_registry import TASK_REGISTRY
from app.db.repositories import (
    create_flow_run,
    update_flow_run_status,
    create_task_run,
)
from app.flows.task_result import TaskResult


def run_flow(flow_def_model, db):
    """
    flow_def_model → SQLAlchemy FlowDefinition object
    db            → SQLAlchemy Session
    """
    flow_id = flow_def_model.id
    flow_def = flow_def_model.definition

    logger.info(f"Starting flow: {flow_id}")

    # -------------------------------------------
    # 1. Create FlowRun
    # -------------------------------------------
    flow_run = create_flow_run(db, flow_id=flow_id)

    context = {}
    executed = []

    current_task = flow_def["start_task"]

    # Convert condition list → dict for fast lookup
    conditions_map = {
        cond["source_task"]: cond
        for cond in flow_def["conditions"]
    }

    # -------------------------------------------
    # 2. Execute Task by Task
    # -------------------------------------------
    while current_task != "end":
        logger.info(f"Running task: {current_task}")

        task_func = TASK_REGISTRY.get(current_task)
        if not task_func:
            logger.error(f"Task not found in registry: {current_task}")
            break

        # Execute the task
        result: TaskResult = task_func(context)

        # Insert into DB via repository
        create_task_run(
            db=db,
            flow_run_id=flow_run.id,
            task_name=current_task,
            success=result.success,
            output=result.data
        )

        executed.append(current_task)
        context[current_task] = result.data

        # Evaluate condition
        cond = conditions_map.get(current_task)
        if not cond:
            logger.info(f"No condition found for task {current_task}, breaking flow.")
            break

        current_task = (
            cond["target_task_success"]
            if result.success
            else cond["target_task_failure"]
        )

    # -------------------------------------------
    # 3. Mark FlowRun Complete
    # -------------------------------------------
    update_flow_run_status(db, flow_run, "completed")

    logger.info(f"Flow {flow_id} completed. Executed: {executed}")

    return {
        "flow_run_id": flow_run.id,
        "executed_tasks": executed,
        "final_output": context.get(executed[-1], {}),
    }
