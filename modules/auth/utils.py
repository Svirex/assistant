from datetime import timedelta, datetime

from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from config import settings
from db import db

from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/auth")

pwd_context = CryptContext(schemes=['bcrypt'])


async def get_user_by_username(username: str):
    return await db.find_one(User, User.username == username)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings['jwt_secret'], algorithms=[settings['jwt']['algorithm']])
        username: str = payload.get('user_id')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user


def hash_password(password):
    return pwd_context.hash(settings['password_salt'] + password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(settings['password_salt'] + plain_password, hashed_password)


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
