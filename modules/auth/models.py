from odmantic import Model, Field


class User(Model):
    username: str
    password_hash: str


class Token(Model):
    access_token: str
    refresh_token: str
