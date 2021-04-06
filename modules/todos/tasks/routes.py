from fastapi import APIRouter

tasks = APIRouter()


@tasks.get('/',
           tags=['Tasks'],
           summary='Получить все задачи пользователя'
           )
async def get_tasks():
    return {"message": "Hello World"}

