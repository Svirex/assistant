from fastapi import FastAPI, Depends, Request
from loguru import logger

from config import settings
from utils.utils import check_token
from modules.todos import todos as todos_routes
from utils.meili_search import Client

app = FastAPI(debug=settings.debug, dependencies=[Depends(check_token)],
              responses={
                  401: {'description': 'Not authorized'}
              })
app.include_router(todos_routes, prefix='/todos')


@app.middleware("http")
async def print_request(request: Request, call_next):
    print(request.headers)
    response = await call_next(request)
    return response


@app.on_event('startup')
async def init_meili_client_and_check_connection():
    app.state.meili_client = Client('http://localhost', 7700)
    is_meili_health = await app.state.meili_client.health()
    if not is_meili_health:
        logger.error('Couldn\'t connect to MeiliSearch by address http://localhost:7700')
        raise ConnectionError('Couldn\'t connect to MeiliSearch by address http://localhost:7700')


@app.on_event('shutdown')
async def close_meili_search_client():
    await app.state.meili_client.close()
