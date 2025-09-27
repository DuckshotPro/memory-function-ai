import asyncio
from mcp.database.db import db_pool, connect_to_db, close_db_connection
from mcp.database.schema import Conversation, Message
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings

async def seed_data():
    await connect_to_db()
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        async with session.begin():
            # Create a new conversation
            conversation = Conversation()
            session.add(conversation)
            await session.flush()

            # Add messages to the conversation
            messages = [
                Message(conversation_id=conversation.id, role="user", content="Hello, world!"),
                Message(conversation_id=conversation.id, role="assistant", content="Hello! How can I help you today?")
            ]
            session.add_all(messages)

    await close_db_connection()
    print("Database seeded with sample data.")

if __name__ == "__main__":
    asyncio.run(seed_data())
