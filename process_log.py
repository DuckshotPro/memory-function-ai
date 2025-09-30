# process_log.py
import sys
import os
import requests

def main():
    """Processes a log file and sends it to the memory-mcp feeder API."""
    if len(sys.argv) < 2:
        print("Usage: python process_log.py <path_to_log_file>")
        sys.exit(1)

    log_file_path = sys.argv[1]

    # --- Configuration ---
    # Get required info from environment variables for security
    feeder_url = os.getenv("FEEDER_URL")
    auth_token = os.getenv("FEEDER_AUTH_TOKEN")

    if not feeder_url or not auth_token:
        print("Error: FEEDER_URL and FEEDER_AUTH_TOKEN environment variables must be set.")
        sys.exit(1)

    api_endpoint = f"{feeder_url.rstrip('/')}/api/ingest"
    headers = {"X-API-Token": auth_token}

    # --- Parse Log File ---
    messages = []
    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                if ':' not in line:
                    continue # Skip lines without a role:content format
                
                role, content = line.split(':', 1)
                # Basic cleaning
                role = role.strip().lower()
                content = content.strip()

                if role and content and role in ['user', 'model', 'system']:
                    messages.append({"role": role, "content": content})

    except FileNotFoundError:
        print(f"Error: Log file not found at {log_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading or parsing log file: {e}")
        sys.exit(1)

    if not messages:
        print("No valid messages found in log file. Nothing to ingest.")
        return

    # --- Send to API ---
    payload = {"messages": messages}
    print(f"Sending {len(messages)} messages to {api_endpoint}...")

    try:
        response = requests.post(api_endpoint, json=payload, headers=headers)
        response.raise_for_status() # Raises an exception for 4xx/5xx errors
        print("API Response:", response.json())
        print("Ingestion successful!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
