#!/bin/bash

# Telegram Music Bot Setup Script
# This script will help you configure the bot with your settings

echo "🎵 Telegram Music Bot Setup"
echo "============================"
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
check_python() {
    print_info "Checking Python installation..."
    if command -v python3.8 &> /dev/null; then
        PYTHON_CMD="python3.8"
        print_info "Python 3.8 found"
    elif command -v python3.9 &> /dev/null; then
        PYTHON_CMD="python3.9"
        print_info "Python 3.9 found"
    elif command -v python3.10 &> /dev/null; then
        PYTHON_CMD="python3.10"
        print_info "Python 3.10 found"
    elif command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
        print_info "Python 3.11 found"
    elif command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if [[ $(echo "$PYTHON_VERSION >= 3.8" | bc -l) -eq 1 ]]; then
            PYTHON_CMD="python3"
            print_info "Python $PYTHON_VERSION found"
        else
            print_error "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3.8 or higher is not installed"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_info "Installing dependencies..."
    
    # Update pip
    $PYTHON_CMD -m pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        $PYTHON_CMD -m pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            print_info "Dependencies installed successfully"
        else
            print_error "Failed to install dependencies"
            exit 1
        fi
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Get bot configuration
get_bot_config() {
    echo "Bot Configuration:"
    echo "=================="
    
    # Get bot token
    read -p "Enter your Telegram Bot Token: " BOT_TOKEN
    while [ -z "$BOT_TOKEN" ]; do
        print_error "Bot Token cannot be empty"
        read -p "Enter your Telegram Bot Token: " BOT_TOKEN
    done
    
    # Get bot username
    read -p "Enter your Bot Username (without @): " BOT_USERNAME
    while [ -z "$BOT_USERNAME" ]; do
        print_error "Bot Username cannot be empty"
        read -p "Enter your Bot Username (without @): " BOT_USERNAME
    done
    
    # Get admin user ID
    read -p "Enter your Telegram User ID (for admin access): " ADMIN_USER_ID
    while [ -z "$ADMIN_USER_ID" ]; do
        print_error "Admin User ID cannot be empty"
        read -p "Enter your Telegram User ID (for admin access): " ADMIN_USER_ID
    done
    
    # Optional: Spotify credentials
    echo
    echo "Optional: Spotify Configuration (for better music metadata)"
    echo "Leave empty if you don't want to use Spotify"
    read -p "Enter Spotify Client ID (optional): " SPOTIFY_CLIENT_ID
    read -p "Enter Spotify Client Secret (optional): " SPOTIFY_CLIENT_SECRET
    
    # Update config file
    update_config_file
}

# Update configuration file
update_config_file() {
    print_info "Updating configuration file..."
    
    # Create backup
    if [ -f "config/config.py" ]; then
        cp config/config.py config/config.py.backup
        print_info "Backup created: config/config.py.backup"
    fi
    
    # Update config file using sed
    sed -i "s/YOUR_TELEGRAM_BOT_TOKEN_HERE/$BOT_TOKEN/" config/config.py
    sed -i "s/YourMusicBot/$BOT_USERNAME/" config/config.py
    sed -i "s/123456789/$ADMIN_USER_ID/" config/config.py
    
    if [ ! -z "$SPOTIFY_CLIENT_ID" ]; then
        sed -i "s/SPOTIFY_CLIENT_ID = \"\"/SPOTIFY_CLIENT_ID = \"$SPOTIFY_CLIENT_ID\"/" config/config.py
    fi
    
    if [ ! -z "$SPOTIFY_CLIENT_SECRET" ]; then
        sed -i "s/SPOTIFY_CLIENT_SECRET = \"\"/SPOTIFY_CLIENT_SECRET = \"$SPOTIFY_CLIENT_SECRET\"/" config/config.py
    fi
    
    print_info "Configuration updated successfully"
}

# Create systemd service file (for Linux)
create_systemd_service() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo
        read -p "Do you want to create a systemd service file? (y/n): " create_service
        if [[ $create_service =~ ^[Yy]$ ]]; then
            print_info "Creating systemd service file..."
            
            SERVICE_FILE="/etc/systemd/system/telegram-music-bot.service"
            CURRENT_DIR=$(pwd)
            
            sudo tee $SERVICE_FILE > /dev/null <<EOL
[Unit]
Description=Telegram Music Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CURRENT_DIR
ExecStart=$PYTHON_CMD src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL
            
            sudo systemctl daemon-reload
            sudo systemctl enable telegram-music-bot.service
            
            print_info "Service file created: $SERVICE_FILE"
            print_info "You can start the bot with: sudo systemctl start telegram-music-bot"
        fi
    fi
}

# Create startup script
create_startup_script() {
    print_info "Creating startup script..."
    
    cat > start_bot.sh << 'EOL'
#!/bin/bash

# Telegram Music Bot Startup Script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the bot
echo "Starting Telegram Music Bot..."
python3 src/main.py
EOL

    chmod +x start_bot.sh
    print_info "Startup script created: start_bot.sh"
}

# Create PythonAnywhere specific files
create_pythonanywhere_files() {
    echo
    read -p "Are you deploying on PythonAnywhere? (y/n): " is_pythonanywhere
    if [[ $is_pythonanywhere =~ ^[Yy]$ ]]; then
        print_info "Creating PythonAnywhere specific files..."
        
        # Create wsgi configuration
        cat > wsgi_config.py << 'EOL'
import sys
import os

# Add the project directory to the Python path
project_home = '/home/your_username/telegram_music_bot'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Change to the project directory
os.chdir(project_home)

# Import the bot application
from src.main import main

# This is the entry point for the PythonAnywhere web app
def application(environ, start_response):
    # For a bot, we don't need a WSGI application
    # We'll run the bot in a separate task
    return main()
EOL

        # Create bash script for PythonAnywhere
        cat > run_bot.sh << 'EOL'
#!/bin/bash

# PythonAnywhere Bot Runner
# This script should be run in a PythonAnywhere task

# Activate virtual environment if it exists
if [ -d "virtualenv" ]; then
    source virtualenv/bin/activate
fi

# Change to project directory
cd /home/your_username/telegram_music_bot

# Start the bot
python3 src/main.py
EOL

        chmod +x run_bot.sh
        print_info "PythonAnywhere files created"
        print_warning "Remember to update the username in wsgi_config.py and run_bot.sh"
    fi
}

# Test configuration
test_configuration() {
    print_info "Testing configuration..."
    
    # Test if config file is valid
    if $PYTHON_CMD -c "import sys; sys.path.append('config'); from config import *; print('Configuration is valid')"; then
        print_info "Configuration test passed"
    else
        print_error "Configuration test failed"
        exit 1
    fi
}

# Main setup process
main() {
    echo "Starting setup process..."
    echo
    
    # Check Python installation
    check_python
    
    # Install dependencies
    install_dependencies
    
    # Get bot configuration
    get_bot_config
    
    # Test configuration
    test_configuration
    
    # Create startup script
    create_startup_script
    
    # Create PythonAnywhere files if needed
    create_pythonanywhere_files
    
    # Create systemd service if on Linux
    create_systemd_service
    
    echo
    echo "🎉 Setup completed successfully!"
    echo
    echo "Next steps:"
    echo "1. Review the configuration in config/config.py"
    echo "2. Run the bot using: ./start_bot.sh"
    echo "3. Or if you created a systemd service: sudo systemctl start telegram-music-bot"
    echo
    echo "For PythonAnywhere deployment:"
    echo "1. Update the username in wsgi_config.py and run_bot.sh"
    echo "2. Upload the files to your PythonAnywhere account"
    echo "3. Create a new task in PythonAnywhere to run ./run_bot.sh"
    echo
    print_info "Don't forget to replace 'your_username' with your actual PythonAnywhere username!"
}

# Run main function
main "$@"