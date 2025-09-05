"""
PythonAnywhere specific configuration and optimizations
This file contains optimizations for running on PythonAnywhere
"""

import os
import sys
import logging
import asyncio
from pathlib import Path

# PythonAnywhere specific settings
PYTHONANYWHERE = True
PYTHONANYWHERE_USERNAME = "your_username"  # Replace with your actual username

# Set up logging for PythonAnywhere
def setup_pythonanywhere_logging():
    """Setup logging optimized for PythonAnywhere"""
    log_dir = Path("/home") / PYTHONANYWHERE_USERNAME / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler(log_dir / "telegram_music_bot.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

# Optimize async settings for PythonAnywhere
def configure_async_settings():
    """Configure async settings for PythonAnywhere environment"""
    # PythonAnywhere has limitations on async operations
    # These settings help optimize performance
    import uvloop
    
    # Use uvloop if available (better performance)
    try:
        uvloop.install()
        print("✅ uvloop installed for better async performance")
    except:
        print("⚠️ uvloop not available, using default event loop")
    
    # Set asyncio settings
    if sys.version_info >= (3, 8):
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

# Optimize file paths for PythonAnywhere
def get_pythonanywhere_paths():
    """Get optimized paths for PythonAnywhere"""
    username = PYTHONANYWHERE_USERNAME
    
    paths = {
        'home': f"/home/{username}",
        'project': f"/home/{username}/telegram_music_bot",
        'downloads': f"/home/{username}/telegram_music_bot/downloads",
        'logs': f"/home/{username}/logs",
        'temp': f"/home/{username}/tmp",
        'virtualenv': f"/home/{username}/.virtualenvs/telegram_music_bot"
    }
    
    # Create directories if they don't exist
    for path in paths.values():
        Path(path).mkdir(parents=True, exist_ok=True)
    
    return paths

# Memory optimization for PythonAnywhere
def optimize_memory_usage():
    """Optimize memory usage for PythonAnywhere"""
    import gc
    
    # Enable garbage collection
    gc.enable()
    
    # Set aggressive garbage collection
    gc.set_threshold(100, 10, 10)
    
    # Limit memory usage for downloads
    import resource
    
    try:
        # Set memory limit to 512MB (PythonAnywhere free tier limit)
        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    except:
        pass  # Ignore if we can't set limits

# Network optimization for PythonAnywhere
def optimize_network_settings():
    """Optimize network settings for PythonAnywhere"""
    import aiohttp
    
    # Configure aiohttp connector for PythonAnywhere
    connector = aiohttp.TCPConnector(
        limit=10,  # Limit concurrent connections
        limit_per_host=5,  # Limit per host
        ttl_dns_cache=300,  # Cache DNS for 5 minutes
        use_dns_cache=True,
    )
    
    return connector

# Download optimization for PythonAnywhere
def optimize_download_settings():
    """Optimize download settings for PythonAnywhere"""
    # PythonAnywhere has bandwidth limitations
    # These settings help work within those limits
    
    download_settings = {
        'timeout': 300,  # 5 minutes timeout
        'retries': 3,  # Number of retries
        'chunk_size': 8192,  # Smaller chunks for better memory management
        'max_file_size': 50 * 1024 * 1024,  # 50MB max file size
    }
    
    return download_settings

# Error handling for PythonAnywhere
class PythonAnywhereErrorHandler:
    """Custom error handler for PythonAnywhere"""
    
    @staticmethod
    def handle_memory_error():
        """Handle memory errors gracefully"""
        logging.error("Memory limit exceeded on PythonAnywhere")
        # Clear some memory
        import gc
        gc.collect()
        
    @staticmethod
    def handle_timeout_error():
        """Handle timeout errors"""
        logging.error("Timeout occurred on PythonAnywhere")
        # Retry with longer timeout
        
    @staticmethod
    def handle_network_error():
        """Handle network errors"""
        logging.error("Network error on PythonAnywhere")
        # Retry with backoff

# Health check for PythonAnywhere
def health_check():
    """Perform health check for PythonAnywhere environment"""
    checks = {
        'disk_space': check_disk_space(),
        'memory_usage': check_memory_usage(),
        'network_connectivity': check_network_connectivity(),
    }
    
    return checks

def check_disk_space():
    """Check available disk space"""
    import shutil
    
    total, used, free = shutil.disk_usage("/home")
    free_mb = free // (1024 * 1024)
    
    if free_mb < 100:  # Less than 100MB
        logging.warning(f"Low disk space: {free_mb}MB free")
        return False
    
    return True

def check_memory_usage():
    """Check memory usage"""
    import psutil
    
    try:
        memory = psutil.virtual_memory()
        if memory.percent > 80:  # More than 80% memory usage
            logging.warning(f"High memory usage: {memory.percent}%")
            return False
        return True
    except:
        return True  # Assume OK if we can't check

def check_network_connectivity():
    """Check network connectivity"""
    import socket
    
    try:
        # Test connection to Telegram API
        socket.create_connection(("api.telegram.org", 443), timeout=5)
        return True
    except:
        logging.error("Network connectivity check failed")
        return False

# Main initialization function
def initialize_pythonanywhere():
    """Initialize PythonAnywhere specific settings"""
    print("🚀 Initializing PythonAnywhere optimization...")
    
    # Setup logging
    logger = setup_pythonanywhere_logging()
    logger.info("PythonAnywhere logging initialized")
    
    # Configure async settings
    configure_async_settings()
    logger.info("Async settings configured")
    
    # Get optimized paths
    paths = get_pythonanywhere_paths()
    logger.info(f"Paths configured: {paths}")
    
    # Optimize memory
    optimize_memory_usage()
    logger.info("Memory optimization completed")
    
    # Optimize network
    connector = optimize_network_settings()
    logger.info("Network optimization completed")
    
    # Get download settings
    download_settings = optimize_download_settings()
    logger.info("Download optimization completed")
    
    # Perform health check
    health = health_check()
    logger.info(f"Health check results: {health}")
    
    print("✅ PythonAnywhere initialization completed")
    
    return {
        'logger': logger,
        'paths': paths,
        'connector': connector,
        'download_settings': download_settings,
        'health': health,
    }

if __name__ == "__main__":
    # Test initialization
    init_result = initialize_pythonanywhere()
    print("Initialization test completed successfully")