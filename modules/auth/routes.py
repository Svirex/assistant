from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from odmantic.exceptions import BaseEngineException, DocumentParsingError

from db import db
from .utils import get_user_by_username, hash_password, verify_password, create_tokens
from .models import User
from .schemas import Registration

auth = APIRouter()


@auth.post('/register', tags=['auth'], status_code=status.HTTP_201_CREATED,
           responses={
               status.HTTP_400_BAD_REQUEST: {
                   'description': 'Username already exist'
               }
           })
async def register(registration_data: Registration):
    try:
        existed_user = await get_user_by_username(registration_data.username)
        if existed_user:
            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error': 'username already exist'})
    except DocumentParsingError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    password_hash = hash_password(registration_data.password.get_secret_value())
    user = User(username=registration_data.username, password_hash=password_hash)
    try:
        await db.save(user)
    except BaseEngineException:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error': 'username already exist'})
    access_token, refresh_token, expire_access = create_tokens({'sub': str(user.id)})
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expire': expire_access,
        'token_type': 'bearer'
    }


@auth.post('/auth', tags=['auth'],
           responses={
               status.HTTP_400_BAD_REQUEST: {
                   'description': 'Invalid username or password'
               }
           })
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = await get_user_by_username(form_data.username)
    if not user:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                              content={'error': 'Invalid username or password'})
    is_correct_password = verify_password(form_data.password, user.password_hash)
    if not is_correct_password:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                              content={'error': 'Invalid username or password'})
    access_token, refresh_token, expire_access = create_tokens({'sub': str(user.id)})
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expire': expire_access,
        'token_type': 'bearer'
    }
