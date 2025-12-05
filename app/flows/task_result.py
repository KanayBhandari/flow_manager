# app/flows/task_result.py

class TaskResult:
    def __init__(self, success: bool, data: dict = None):
        self.success = success
        self.data = data or {}