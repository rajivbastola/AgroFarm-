import logging
import sys
from pathlib import Path
from loguru import logger
from fastapi import Request
from typing import Callable
import time
import json

# Configure Loguru logger
LOG_LEVEL = "INFO"
LOG_PATH = Path("logs")
LOG_PATH.mkdir(exist_ok=True)

# Remove default logger
logger.remove()

# Add console logger
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level=LOG_LEVEL,
    colorize=True
)

# Add file logger for errors
logger.add(
    LOG_PATH / "error.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="ERROR",
    rotation="1 day",
    retention="30 days"
)

# Add file logger for access logs
logger.add(
    LOG_PATH / "access.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
    level="INFO",
    filter=lambda record: "access" in record["extra"],
    rotation="1 day",
    retention="30 days"
)

class RequestLoggingMiddleware:
    """Middleware for logging requests and responses"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request: Request, call_next: Callable):
        # Start timer
        start_time = time.time()
        
        # Prepare request logging info
        method = request.method
        url = str(request.url)
        client_ip = request.client.host
        
        response = None
        try:
            response = await call_next(request)
            
            # Log successful request
            duration = time.time() - start_time
            status_code = response.status_code
            
            log_data = {
                "client_ip": client_ip,
                "method": method,
                "url": url,
                "status_code": status_code,
                "duration": f"{duration:.3f}s"
            }
            
            logger.bind(access=True).info(json.dumps(log_data))
            
            return response
            
        except Exception as e:
            # Log error
            logger.error(
                f"Request failed: {method} {url}\n"
                f"Client IP: {client_ip}\n"
                f"Error: {str(e)}"
            )
            raise
        
        finally:
            # Always log response time
            if response:
                response.headers["X-Process-Time"] = str(time.time() - start_time)

def setup_logging():
    """Initialize logging configuration"""
    # Suppress uvicorn access logging as we have our own
    logging.getLogger("uvicorn.access").handlers = []
    
    # Set SQLAlchemy logging to warning level
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)