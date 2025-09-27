import pytest
from unittest.mock import MagicMock
from mcp_server.mcp.summarize import summarize_messages
from mcp_server.mcp.database.schema import Message

@pytest.mark.asyncio
async def test_summarize_messages():
    # Arrange
    mock_adapter = MagicMock()
    mock_adapter.send_message = MagicMock(return_value="This is a summary.")

    messages = [
        Message(role="user", content="Hello"),
        Message(role="assistant", content="Hi there")
    ]

    # Act
    summary = await summarize_messages(messages, llm_adapter=mock_adapter)

    # Assert
    assert summary == "This is a summary."
    # Check that the adapter was called with a prompt containing the transcript
    mock_adapter.send_message.assert_called_once()
    call_args = mock_adapter.send_message.call_args[0][0]
    assert "user: Hello" in call_args
    assert "assistant: Hi there" in call_args
