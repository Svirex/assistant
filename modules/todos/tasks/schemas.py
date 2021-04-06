from typing import Optional
from pydantic import BaseModel, Field


class TaskAdditional(BaseModel):
    description: Optional[str] = Field(..., description='Описание задачи')


class Task(TaskAdditional):
    task: str = Field(..., description='Название задачи')


class TaskUpdate(TaskAdditional):
    task: Optional[str] = Field(..., description='Название задачи')
