import os
import time
import asyncio
from google.adk.agents import Agent
from memory_tool import log_to_database

# --- Configuration ---
FILE_TO_WATCH = "/var/data/gemini/GEMINI.md"
POLL_INTERVAL_SECONDS = 5

class ConversationLoggerAgent:
    def __init__(self):
        self._agent = Agent(
            name="conversation_logger",
            instruction="Your job is to log conversation snippets to a database using the provided tool.",
            tools=[log_to_database]
        )
        self._last_seen_timestamp = 0
        self._last_content = ""

    def _read_new_content(self) -> str | None:
        try:
            current_timestamp = os.path.getmtime(FILE_TO_WATCH)
            if current_timestamp > self._last_seen_timestamp:
                with open(FILE_TO_WATCH, 'r') as f:
                    full_content = f.read()
                
                if self._last_content in full_content:
                    new_content = full_content[len(self._last_content):]
                else:
                    new_content = full_content

                self._last_seen_timestamp = current_timestamp
                self._last_content = full_content
                return new_content.strip()
        except FileNotFoundError:
            self._last_seen_timestamp = 0
            self._last_content = ""
        return None

    async def run_loop(self):
        print(f"Starting conversation logger. Watching file: {FILE_TO_WATCH}")
        while True:
            new_content = self._read_new_content()
            if new_content:
                print("Detected new content. Logging to database...")
                response = await self._agent.send_message(
                    f'Log the following conversation snippet: "{new_content}'
                )
                if response.tool_calls:
                    for call in response.tool_calls:
                        print(f"Tool call result: {call.result}")
                else:
                    print(f"Agent response: {response.text}")
            
            time.sleep(POLL_INTERVAL_SECONDS)

async def main():
    logger_agent = ConversationLoggerAgent()
    await logger_agent.run_loop()

if __name__ == "__main__":
    asyncio.run(main())
