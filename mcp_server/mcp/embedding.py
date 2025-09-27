import google.generativeai as genai
import asyncio

async def generate_embedding(text: str) -> list[float]:
    """Generates an embedding for the given text using the Google AI API."""
    try:
        loop = asyncio.get_running_loop()
        # Use run_in_executor to avoid blocking the event loop with a sync call
        result = await loop.run_in_executor(
            None, lambda: genai.embed_content(model='models/embedding-001', content=text)
        )
        return result['embedding']
    except Exception as e:
        print(f"An error occurred during embedding generation: {e}")
        return None
