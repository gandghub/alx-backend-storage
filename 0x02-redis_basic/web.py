#!/usr/bin/env python3
""" Expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """Decorator to cache requests and count URL accesses"""

    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapper that caches results and tracks access count"""
        # Increment the URL access count
        redis.incr(f"count:{url}")

        # Check if the result is already cached
        cached_response = redis.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')

        # Get the result from the function if not cached
        result = fn(url)
        # Cache the result with a 10-second expiration
        redis.setex(f"cached:{url}", 10, result)

        return result

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """Fetches the page content from the URL"""
    response = requests.get(url)
    return response.text
