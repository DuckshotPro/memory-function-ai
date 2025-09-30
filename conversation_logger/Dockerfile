FROM python:3.11-slim

WORKDIR /app

# Copy the worker's python code into the container
COPY . .

# Install dependencies from PyPI
RUN pip install --no-cache-dir google-adk requests

# Command to run the agent
CMD ["python", "conversation_logger.py"]
