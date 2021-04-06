from passlib.context import CryptContext

from config import settings
from db import db

from .models import User

pwd_context = CryptContext(schemes=['bcrypt'])


async def get_user_by_username(username: str):
    return await db.find_one(User, User.username == username)


def hash_password(password):
    return pwd_context.hash(settings['password_salt'] + password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(settings['password_salt'] + plain_password, hashed_password)


