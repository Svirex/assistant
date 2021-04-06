from fastapi import APIRouter

from .tasks.routes import tasks

todos = APIRouter()

todos.include_router(tasks, prefix='/tasks')
