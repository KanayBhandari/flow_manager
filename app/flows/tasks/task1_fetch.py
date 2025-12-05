from app.flows.task_result import TaskResult

def task1_fetch(context: dict):
    # Simulate fetching data
    return TaskResult(success=True, data={"fetched_value": 100})
