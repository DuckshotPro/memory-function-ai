from .adapters.base import BaseAdapter
from .adapters.gemini import GeminiAdapter
from .database.schema import Message
from typing import List

async def summarize_messages(messages: List[Message], llm_adapter: BaseAdapter = None) -> str:
    """
    Summarizes a list of conversation messages into concise cliff notes.

    Args:
        messages: A list of Message objects to be summarized.
        llm_adapter: An optional LLM adapter. If not provided, a new GeminiAdapter is created.

    Returns:
        A string containing the summarized cliff notes.
    """
    if not messages:
        return "No messages to summarize."

    # For simplicity, create a new adapter if one isn't provided.
    # In a larger app, you might want to manage this via dependency injection.
    if llm_adapter is None:
        llm_adapter = GeminiAdapter()

    # Format the messages into a simple transcript.
    transcript = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])

    # Create a specific prompt for summarization.
    prompt = f"""Provide a concise summary (like 'cliff notes') of the key points and topics in the following conversation transcript. 
    Do not add any preamble or conversational text. Output only the summary.

    Transcript:
    ---
    {transcript}
    ---

    Summary:"""

    # Use the LLM to generate the summary.
    summary = await llm_adapter.send_message(prompt)
    return summary
