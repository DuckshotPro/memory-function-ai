from google.adk.tools import tool
import requests
import os

@tool
def log_to_database(conversation_content: str) -> str:
    """
    Logs the given content to the memory database by sending it to the chat API.

    Args:
        conversation_content: The text content to be logged.
    
    Returns:
        A string indicating the result of the operation.
    """
    api_base = os.environ.get('MEMORY_API_URL', 'http://localhost:8000')
    headers = {'Content-Type': 'application/json'}
    payload = {'message': conversation_content}

    try:
        response = requests.post(f'{api_base}/chat', json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return f"Successfully logged content. Response: {response.json().get('response')}"
        else:
            return f"Failed to log content. Status: {response.status_code}, Body: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Connection error: {e}"
