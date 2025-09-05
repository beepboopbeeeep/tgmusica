"""
WSGI configuration for PythonAnywhere
This file is used by PythonAnywhere to run the bot
"""

import os
import sys
import logging
import threading
import time
from pathlib import Path

# Add project directory to Python path
project_home = '/home/your_username/telegram_music_bot'  # Replace with your username
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Change to project directory
os.chdir(project_home)

# Import PythonAnywhere optimizations
try:
    from src.pythonanywhere_optimization import initialize_pythonanywhere
    pythonanywhere_config = initialize_pythonanywhere()
    logger = pythonanywhere_config['logger']
except ImportError:
    # Fallback logging if optimization module not available
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

# Global bot instance
bot_instance = None
bot_thread = None

def run_bot():
    """Run the Telegram bot"""
    global bot_instance
    
    try:
        logger.info("Starting Telegram Music Bot...")
        
        # Import and run the bot
        from src.main import main
        main()
        
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        # Wait before restarting
        time.sleep(30)
        # Try to restart
        run_bot()

def start_bot_thread():
    """Start the bot in a separate thread"""
    global bot_thread
    
    if bot_thread is None or not bot_thread.is_alive():
        logger.info("Starting bot thread...")
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        logger.info("Bot thread started")

# WSGI application (required by PythonAnywhere)
def application(environ, start_response):
    """
    WSGI application entry point
    This is required by PythonAnywhere but not used for the bot
    """
    
    # Start the bot thread if not already running
    start_bot_thread()
    
    # Return a simple response
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    
    return [b"Telegram Music Bot is running"]

# Health check endpoint
def health_check():
    """Health check function"""
    try:
        # Check if bot thread is running
        if bot_thread and bot_thread.is_alive():
            return {"status": "healthy", "bot_running": True}
        else:
            return {"status": "unhealthy", "bot_running": False}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# For direct execution
if __name__ == "__main__":
    print("Starting WSGI application...")
    start_bot_thread()
    print("Bot started in background thread")
    
    # Keep the script running
    try:
        while True:
            time.sleep(60)
            # Perform health check
            health = health_check()
            logger.info(f"Health check: {health}")
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        sys.exit(0)