#!/bin/bash

# Unified Dashboard Startup Script
# Starts all automation systems and the dashboard

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_DIR="$SCRIPT_DIR/pids"
LOG_DIR="$SCRIPT_DIR/logs"

# Create directories
mkdir -p "$PID_DIR" "$LOG_DIR"

echo -e "${BLUE}🚀 Starting Unified Automation Dashboard${NC}"
echo "=============================================="

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Function to start automation script
start_automation() {
    local name=$1
    local script=$2
    local args=${3:-}

    if [[ -f "$PID_DIR/${name}.pid" ]]; then
        local pid=$(cat "$PID_DIR/${name}.pid")
        if kill -0 "$pid" 2>/dev/null; then
            warn "$name is already running (PID: $pid)"
            return
        else
            rm -f "$PID_DIR/${name}.pid"
        fi
    fi

    log "Starting $name automation..."

    if [[ "$script" == *.py ]]; then
        nohup python3 "$script" $args > "$LOG_DIR/${name}.log" 2>&1 &
    elif [[ "$script" == *.js ]]; then
        nohup node "$script" $args > "$LOG_DIR/${name}.log" 2>&1 &
    else
        nohup "$script" $args > "$LOG_DIR/${name}.log" 2>&1 &
    fi

    local pid=$!
    echo $pid > "$PID_DIR/${name}.pid"

    # Verify it started
    sleep 2
    if kill -0 "$pid" 2>/dev/null; then
        log "$name started successfully (PID: $pid)"
    else
        error "$name failed to start"
        rm -f "$PID_DIR/${name}.pid"
    fi
}

# Function to stop automation
stop_automation() {
    local name=$1

    if [[ -f "$PID_DIR/${name}.pid" ]]; then
        local pid=$(cat "$PID_DIR/${name}.pid")
        if kill -0 "$pid" 2>/dev/null; then
            log "Stopping $name (PID: $pid)..."
            kill "$pid"

            # Wait for graceful shutdown
            local count=0
            while kill -0 "$pid" 2>/dev/null && [[ $count -lt 10 ]]; do
                sleep 1
                ((count++))
            done

            # Force kill if still running
            if kill -0 "$pid" 2>/dev/null; then
                warn "Force killing $name..."
                kill -9 "$pid"
            fi

            rm -f "$PID_DIR/${name}.pid"
            log "$name stopped"
        else
            warn "$name was not running"
            rm -f "$PID_DIR/${name}.pid"
        fi
    else
        warn "No PID file found for $name"
    fi
}

# Function to check if script exists
check_script() {
    local script=$1
    if [[ ! -f "$script" ]]; then
        warn "Script not found: $script (will be skipped)"
        return 1
    fi
    return 0
}

# Install dependencies if needed
install_dependencies() {
    log "Checking dependencies..."

    # Check Python dependencies
    if ! python3 -c "import flask, flask_socketio, psutil" 2>/dev/null; then
        log "Installing Python dependencies..."
        pip3 install flask flask-socketio flask-cors psutil python-socketio
    fi
}

# Main startup function
start_all() {
    log "Starting all automation systems..."

    install_dependencies

    # Start MCP server
    if check_script "simple_server.py"; then
        start_automation "mcp_server" "simple_server.py"
    fi

    # Start existing automations (check if they exist first)
    if check_script "calendar_automation.py"; then
        start_automation "calendar" "calendar_automation.py"
    fi

    if check_script "email_backlog.py"; then
        start_automation "email" "email_backlog.py"
    fi

    if check_script "client_retrieval.py"; then
        start_automation "client" "client_retrieval.py"
    fi

    # Start new marketing automations
    if check_script "automation_main.py"; then
        start_automation "marketing" "automation_main.py"
    fi

    if check_script "lead_scoring.py"; then
        start_automation "scoring" "lead_scoring.py"
    fi

    if check_script "quote_generation.py"; then
        start_automation "quotes" "quote_generation.py"
    fi

    # Start dashboard backend
    if check_script "dashboard_backend.py"; then
        start_automation "dashboard" "dashboard_backend.py"
        sleep 3  # Give dashboard time to start

        log "Dashboard available at: http://localhost:5000"
        log "MCP Server running for Claude integration"
        log "WebSocket endpoint: ws://localhost:5000"
    fi

    # Show status
    show_status
}

# Stop all automations
stop_all() {
    log "Stopping all automation systems..."

    local automations=("dashboard" "quotes" "scoring" "marketing" "client" "email" "calendar" "mcp_server")

    for automation in "${automations[@]}"; do
        stop_automation "$automation"
    done

    log "All systems stopped"
}

# Show status of all systems
show_status() {
    echo
    echo -e "${BLUE}📊 System Status:${NC}"
    echo "==================="

    local total_running=0
    local automations=("mcp_server" "calendar" "email" "client" "marketing" "scoring" "quotes" "dashboard")

    for automation in "${automations[@]}"; do
        if [[ -f "$PID_DIR/${automation}.pid" ]]; then
            local pid=$(cat "$PID_DIR/${automation}.pid")
            if kill -0 "$pid" 2>/dev/null; then
                echo -e "${GREEN}✓${NC} $automation (PID: $pid)"
                ((total_running++))
            else
                echo -e "${RED}✗${NC} $automation (dead)"
                rm -f "$PID_DIR/${automation}.pid"
            fi
        else
            echo -e "${YELLOW}○${NC} $automation (not started)"
        fi
    done

    echo
    echo -e "Running: ${GREEN}$total_running${NC} / ${#automations[@]} systems"

    if [[ -f "$PID_DIR/dashboard.pid" ]]; then
        local dashboard_pid=$(cat "$PID_DIR/dashboard.pid")
        if kill -0 "$dashboard_pid" 2>/dev/null; then
            echo -e "\n${GREEN}🌐 Dashboard: http://localhost:5000${NC}"
        fi
    fi

    if [[ -f "$PID_DIR/mcp_server.pid" ]]; then
        local mcp_pid=$(cat "$PID_DIR/mcp_server.pid")
        if kill -0 "$mcp_pid" 2>/dev/null; then
            echo -e "${GREEN}🔌 MCP Server: Ready for Claude integration${NC}"
        fi
    fi
}

# Main command processing
case "${1:-start}" in
    start)
        start_all
        ;;
    stop)
        stop_all
        ;;
    restart)
        stop_all
        sleep 3
        start_all
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        echo ""
        echo "Commands:"
        echo "  start    - Start all automation systems and dashboard"
        echo "  stop     - Stop all automation systems"
        echo "  restart  - Restart all systems"
        echo "  status   - Show status of all systems"
        ;;
esac