from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

_client = None
_db = None


async def connect_db():
    global _client, _db
    _client = AsyncIOMotorClient(settings.mongodb_uri)
    _db = _client["content_strategy_db"]
    print("Connected to MongoDB")


async def disconnect_db():
    global _client
    if _client:
        _client.close()
        print("Disconnected from MongoDB")


def get_db():
    return _db
