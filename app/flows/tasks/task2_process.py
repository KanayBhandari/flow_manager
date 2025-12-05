from app.flows.task_result import TaskResult

def task2_process(context: dict):
    try:
        value = context["task1"]["fetched_value"] * 2
        return TaskResult(success=True, data={"processed_value": value})
    except:
        return TaskResult(success=False)
