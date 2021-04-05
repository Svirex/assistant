from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from config import settings

client = AsyncIOMotorClient(settings['mongo']['server'], settings['mongo']['port'])
db = AIOEngine(motor_client=client, database=settings['mongo']['db'])
