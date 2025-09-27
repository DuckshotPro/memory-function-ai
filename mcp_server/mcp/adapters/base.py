from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    """
    This is the abstract base class for all Large Language Model (LLM) adapters.
    To add support for a new LLM, you should create a new class that inherits from this one.

    Example of a new adapter:
    --------------------------
    
    from .base import BaseAdapter

    class MyNewLlmAdapter(BaseAdapter):
        def __init__(self, api_key: str):
            self.api_key = api_key
            # ... other initialization ...

        async def send_message(self, message: str) -> str:
            # ... implementation to call the new LLM's API ...
            response = await my_llm_api_call(message, self.api_key)
            return response

    Then, you can instantiate your new adapter in `mcp_server/mcp/server.py`.
    """

    @abstractmethod
    async def send_message(self, message: str) -> str:
        """Sends a message to the LLM and returns the response."""
        pass