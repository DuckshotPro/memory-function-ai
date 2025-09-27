import asyncpg
from config import settings

db_pool = None

async def connect_to_db():
    global db_pool
    db_pool = await asyncpg.create_pool(dsn=settings.database_url)

async def close_db_connection():
    await db_pool.close()
