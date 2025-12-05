from app.flows.task_result import TaskResult

def task3_store(context: dict):
    # Simulate persisting
    return TaskResult(success=True, data={"stored": True})
