from .auth.models import User


async def ensure_indexes():
    await User.ensure_indexes()
