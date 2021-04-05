from fastapi import FastAPI, Depends

from config import settings
from modules.auth.routes import auth as auth_routes
from modules.auth.utils import get_current_user
from modules.todos import todos as todos_routes

app = FastAPI(debug=settings.debug)

app.include_router(todos_routes, prefix='/todos', dependencies=[Depends(get_current_user)],
                   responses={
                       401: {
                           'description': 'Not authorized'
                       }
                   })
app.include_router(auth_routes, prefix='/auth')



