import motor.motor_asyncio
from .config import settings
from aioredis import Redis
from aioredis.exceptions import RedisError

from typing import Optional

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)

db = client[settings.db_name]
affiliate_db = db.affiliate
advitisor_db = db.advitisor
payment_details_db = db.payment_details
transaction_db = db.transactions
manager_db=db.manager

base_db = client[settings.affilator_base_db]
click_db = base_db.clicks
transactions_db = base_db.transactions
campaign_db = base_db.campaign
approve_db=base_db.approve

class RedisClient(object):
    redis_client: Redis

    @classmethod
    async def connect_redis(cls, url: str):
        cls.redis_client = Redis.from_url(
            settings.redis_url,
            encoding="utf-8",
        )
        await cls.redis_client.ping()

    @classmethod
    async def ping(cls) -> bool:
        try:
            return await cls.redis_client.ping()
        except RedisError as err:
            print(err)
        return False

    @classmethod
    async def set(cls, key: str, value: str, exp: Optional[int] = None) -> bool:
        try:
            return await cls.redis_client.set(name=key, value=value, ex=exp)
        except RedisError as err:
            print(err)
        return False

    @classmethod
    async def get(cls, key: str) -> str:
        try:
            res = await cls.redis_client.get(name=key)
            return "" if not res else res
        except RedisError as err:
            print(err)
