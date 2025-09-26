from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    @abstractmethod
    async def send_message(self, message: str) -> str:
        """Sends a message to the LLM and returns the response."""
        pass
