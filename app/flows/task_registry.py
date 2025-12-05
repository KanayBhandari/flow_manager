from app.flows.tasks.task1_fetch import task1_fetch
from app.flows.tasks.task2_process import task2_process
from app.flows.tasks.task3_store import task3_store

TASK_REGISTRY = {
    "task1": task1_fetch,
    "task2": task2_process,
    "task3": task3_store
}
