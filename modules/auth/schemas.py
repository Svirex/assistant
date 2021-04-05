from pydantic import BaseModel, SecretStr, validator

from config import settings


class Registration(BaseModel):
    username: str
    password: SecretStr
    repeat_password: SecretStr

    @validator('password')
    def check_length(cls, password):
        if len(password) < settings['password_length']:
            raise ValueError(f'length password must be {settings["password_length"]} or greater')
        return password

    @validator('repeat_password')
    def passwords_match(cls, repeat_password, values, **kwargs):
        if 'password' in values and repeat_password != values['password']:
            raise ValueError('passwords do not match')
        return repeat_password
