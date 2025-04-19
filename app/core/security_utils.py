from fastapi import HTTPException, Request
from typing import Callable, Optional
import time
from datetime import datetime, timedelta
from cachetools import TTLCache
from collections import defaultdict

# Rate limiting configuration
RATE_LIMIT_DURATION = 60  # seconds
MAX_REQUESTS = 100  # requests per duration
rate_limit_store = defaultdict(lambda: {"count": 0, "reset_time": time.time()})

# Cache configuration
cache = TTLCache(maxsize=100, ttl=300)  # 5 minutes TTL

def rate_limit(max_requests: int = MAX_REQUESTS, duration: int = RATE_LIMIT_DURATION):
    """Rate limiting decorator for API endpoints"""
    def decorator(func: Callable):
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host
            current_time = time.time()
            
            # Reset rate limit if duration has passed
            if current_time - rate_limit_store[client_ip]["reset_time"] >= duration:
                rate_limit_store[client_ip] = {
                    "count": 0,
                    "reset_time": current_time
                }
            
            # Increment request count
            rate_limit_store[client_ip]["count"] += 1
            
            # Check if rate limit exceeded
            if rate_limit_store[client_ip]["count"] > max_requests:
                reset_time = datetime.fromtimestamp(
                    rate_limit_store[client_ip]["reset_time"] + duration
                )
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Try again after {reset_time}"
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

def cache_response(
    expire_after_seconds: int = 300,
    key_prefix: str = "",
    vary_on_headers: Optional[list[str]] = None
):
    """Caching decorator for API endpoints"""
    def decorator(func: Callable):
        async def wrapper(request: Request, *args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{request.url.path}"
            
            # Add query params to cache key
            if request.url.query:
                cache_key += f"?{request.url.query}"
            
            # Add headers to cache key if specified
            if vary_on_headers:
                for header in vary_on_headers:
                    if header in request.headers:
                        cache_key += f":{header}={request.headers[header]}"
            
            # Return cached response if exists
            if cache_key in cache:
                return cache[cache_key]
            
            # Generate and cache response
            response = await func(request, *args, **kwargs)
            cache[cache_key] = response
            return response
        
        return wrapper
    return decorator

def clear_cache_for_prefix(prefix: str):
    """Clear all cached items with given prefix"""
    keys_to_delete = [
        k for k in cache.keys()
        if k.startswith(prefix)
    ]
    for k in keys_to_delete:
        cache.pop(k, None)