from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .database.schema import Message
from .embedding import generate_embedding
from config import settings

async def find_relevant_messages(query_text: str, limit: int = 5):
    """Finds relevant messages in the database using vector similarity search."""
    query_embedding = await generate_embedding(query_text)
    if not query_embedding:
        return []

    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # The l2_distance operator (<->) is provided by pgvector
        results = await session.query(Message).order_by(Message.embedding.l2_distance(query_embedding)).limit(limit).all()
        return results
