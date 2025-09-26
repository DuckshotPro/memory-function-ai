import google.generativeai as genai
from .base import BaseAdapter
from config import settings
import asyncio

class GeminiAdapter(BaseAdapter):
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def send_message(self, message: str) -> str:
        """Sends a message to the Gemini API and returns the response."""
        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None, self.model.generate_content, message
            )
            return response.text
        except Exception as e:
            return f"An error occurred with the Gemini API: {e}"
