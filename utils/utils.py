from datetime import timedelta, datetime

from fastapi import HTTPException, Header
from jose import jwt, JWTError
from starlette import status

from config import settings


async def check_token(auth_data: str = Header(..., alias='Authorization')):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    splitted_data = auth_data.split(" ")
    if len(splitted_data) != 2 or splitted_data[0].lower() != 'bearer':
        raise credentials_exception
    try:
        jwt.decode(splitted_data[1], settings['jwt_secret'], algorithms=[settings['jwt']['algorithm']])
    except JWTError:
        raise credentials_exception


def create_single_token(data: dict, expire_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings['jwt_secret'], algorithm=settings['jwt']['algorithm'])
    return encoded_jwt, expire


def create_tokens(data: dict):
    access_token, expire_access = create_single_token(data, expire_delta=timedelta(
        minutes=settings['jwt']['access_expire_delta']))
    refresh_token, _ = create_single_token(data,
                                           expire_delta=timedelta(minutes=settings['jwt']['refresh_expire_delta']))
    return access_token, refresh_token, expire_access