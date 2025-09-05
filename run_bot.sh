#!/bin/bash

# PythonAnywhere Bot Runner Script
# This script runs the Telegram bot on PythonAnywhere

# Configuration
PYTHONANYWHERE_USERNAME="your_username"  # Replace with your actual username
PROJECT_DIR="/home/$PYTHONANYWHERE_USERNAME/telegram_music_bot"
VENV_DIR="/home/$PYTHONANYWHERE_USERNAME/.virtualenvs/telegram_music_bot"
LOG_DIR="/home/$PYTHONANYWHERE_USERNAME/logs"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO:${NC} $1"
}

# Check if we're on PythonAnywhere
check_pythonanywhere() {
    if [[ ! "$HOME" == *"/home/"* ]]; then
        error "This script is designed to run on PythonAnywhere"
        exit 1
    fi
    
    info "Running on PythonAnywhere"
}

# Setup environment
setup_environment() {
    info "Setting up environment..."
    
    # Change to project directory
    cd "$PROJECT_DIR" || {
        error "Failed to change to project directory: $PROJECT_DIR"
        exit 1
    }
    
    # Activate virtual environment
    if [[ -d "$VENV_DIR" ]]; then
        source "$VENV_DIR/bin/activate"
        info "Virtual environment activated"
    else
        warning "Virtual environment not found. Creating one..."
        python3.8 -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
        pip install --upgrade pip
        pip install -r requirements.txt
        info "Virtual environment created and activated"
    fi
    
    # Create log directory
    mkdir -p "$LOG_DIR"
    info "Log directory created"
}

# Check dependencies
check_dependencies() {
    info "Checking dependencies..."
    
    # Check Python version
    python_version=$(python3 --version 2>&1)
    info "Python version: $python_version"
    
    # Check required packages
    required_packages=("python-telegram-bot" "shazamio" "yt-dlp" "requests")
    for package in "${required_packages[@]}"; do
        if python -c "import $package" 2>/dev/null; then
            info "✅ $package is installed"
        else
            warning "⚠️ $package is not installed. Installing..."
            pip install "$package"
        fi
    done
}

# Check configuration
check_configuration() {
    info "Checking configuration..."
    
    # Check if config file exists
    if [[ ! -f "config/config.py" ]]; then
        error "Configuration file not found: config/config.py"
        exit 1
    fi
    
    # Check if bot token is configured
    if grep -q "YOUR_TELEGRAM_BOT_TOKEN_HERE" config/config.py; then
        error "Bot token is not configured in config/config.py"
        info "Please run the setup script first: ./setup.sh"
        exit 1
    fi
    
    info "✅ Configuration is valid"
}

# Clean up old files
cleanup() {
    info "Cleaning up old files..."
    
    # Clean downloads directory
    if [[ -d "downloads" ]]; then
        find downloads -type f -mtime +1 -delete 2>/dev/null || true
        info "Cleaned old downloads"
    fi
    
    # Clean log files older than 7 days
    if [[ -d "$LOG_DIR" ]]; then
        find "$LOG_DIR" -name "*.log" -mtime +7 -delete 2>/dev/null || true
        info "Cleaned old log files"
    fi
}

# Health check
health_check() {
    info "Performing health check..."
    
    # Check disk space
    disk_usage=$(df -h "$PROJECT_DIR" | tail -1 | awk '{print $5}' | sed 's/%//')
    if [[ $disk_usage -gt 90 ]]; then
        warning "High disk usage: ${disk_usage}%"
    else
        info "✅ Disk usage: ${disk_usage}%"
    fi
    
    # Check memory usage
    if command -v free &> /dev/null; then
        memory_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
        if [[ $memory_usage -gt 80 ]]; then
            warning "High memory usage: ${memory_usage}%"
        else
            info "✅ Memory usage: ${memory_usage}%"
        fi
    fi
    
    # Check if bot is running
    if pgrep -f "python.*main.py" > /dev/null; then
        info "✅ Bot is running"
    else
        warning "⚠️ Bot is not running"
    fi
}

# Start bot
start_bot() {
    info "Starting Telegram Music Bot..."
    
    # Change to project directory
    cd "$PROJECT_DIR"
    
    # Set environment variables for PythonAnywhere
    export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"
    export PYTHONUNBUFFERED=1
    
    # Start the bot with error handling
    while true; do
        info "Starting bot process..."
        
        # Run the bot
        python src/main.py >> "$LOG_DIR/telegram_music_bot.log" 2>&1
        
        # Check exit code
        exit_code=$?
        if [[ $exit_code -eq 0 ]]; then
            info "Bot exited normally"
            break
        else
            error "Bot crashed with exit code $exit_code"
            info "Restarting in 30 seconds..."
            sleep 30
        fi
        
        # Perform health check before restart
        health_check
    done
}

# Stop bot
stop_bot() {
    info "Stopping bot..."
    
    # Find and kill bot processes
    pkill -f "python.*main.py" || true
    pkill -f "telegram.*bot" || true
    
    info "Bot stopped"
}

# Main function
main() {
    info "=== Telegram Music Bot Runner ==="
    
    # Check if we're on PythonAnywhere
    check_pythonanywhere
    
    # Parse command line arguments
    case "${1:-start}" in
        "start")
            setup_environment
            check_dependencies
            check_configuration
            cleanup
            health_check
            start_bot
            ;;
        "stop")
            stop_bot
            ;;
        "restart")
            stop_bot
            sleep 5
            setup_environment
            check_dependencies
            check_configuration
            cleanup
            health_check
            start_bot
            ;;
        "health")
            setup_environment
            health_check
            ;;
        "setup")
            setup_environment
            check_dependencies
            check_configuration
            ;;
        "cleanup")
            cleanup
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|health|setup|cleanup}"
            echo "  start   - Start the bot"
            echo "  stop    - Stop the bot"
            echo "  restart - Restart the bot"
            echo "  health  - Perform health check"
            echo "  setup   - Setup environment"
            echo "  cleanup - Clean up old files"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"