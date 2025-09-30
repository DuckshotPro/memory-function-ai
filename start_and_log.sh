#!/bin/bash

# This script starts a logged session and processes the log file upon exit.

# --- Configuration ---
export FEEDER_URL="https://conversation-feeder.onrender.com"
export FEEDER_AUTH_TOKEN="8919847d840e37b3aa2525b3c2a00223"

# --- Script Logic ---

# Default log file name with a timestamp
DEFAULT_LOG_FILE="chat_session_$(date +%Y-%m-%d_%H-%M-%S).log"
LOG_FILE=${1:-$DEFAULT_LOG_FILE}

PYTHON_SCRIPT_PATH="$(dirname "$0")/process_log.py"

# Inform the user
echo "---------------------------------------------------------------------"
echo "Starting logged session. Log file: $LOG_FILE"
echo "To end this session and upload the log, simply type: exit"
echo "---------------------------------------------------------------------"
echo

# Start a new shell session and record it. The script will wait here until
# the user types 'exit' in the new shell.
# The `-q` flag makes it quiet (no start/end messages from `script` itself)
script -q "$LOG_FILE"

# This part runs only after the user has typed 'exit'
echo
echo "---------------------------------------------------------------------"
echo "Session ended. Processing log file to upload to Memory MCP..."
echo "---------------------------------------------------------------------"

# Run the python script to process the log file
python3 "$PYTHON_SCRIPT_PATH" "$LOG_FILE"

# Unset the secrets
unset FEEDER_URL
unset FEEDER_AUTH_TOKEN

echo "
Process complete."
