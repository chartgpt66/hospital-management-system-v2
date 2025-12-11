import json
from functools import wraps
from flask import current_app
from app import redis_client

def cache_key(*args, **kwargs):
    """Generate cache key from arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
    return ":".join(key_parts)

def cached(prefix, timeout=300):
    """Decorator to cache function results in Redis"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            key = f"{prefix}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            try:
                cached_data = redis_client.get(key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                current_app.logger.error(f"Cache read error: {e}")
            
            # Execute function
            result = f(*args, **kwargs)
            
            # Store in cache
            try:
                redis_client.setex(key, timeout, json.dumps(result))
            except Exception as e:
                current_app.logger.error(f"Cache write error: {e}")
            
            return result
        return decorated_function
    return decorator

def invalidate_cache(prefix, *args, **kwargs):
    """Invalidate cache for specific key"""
    key = f"{prefix}:{cache_key(*args, **kwargs)}"
    try:
        redis_client.delete(key)
    except Exception as e:
        current_app.logger.error(f"Cache invalidation error: {e}")

def invalidate_pattern(pattern):
    """Invalidate all cache keys matching pattern"""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception as e:
        current_app.logger.error(f"Cache pattern invalidation error: {e}")
