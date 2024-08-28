#!/usr/bin/env python3
"""
Caching request module.
"""
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize the Redis client
rc = redis.Redis()

def track_get_page(fn: Callable) -> Callable:
    """Decorator for get_page.
    Tracks how many times a URL has been accessed and caches the content.
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapper that:
        - Checks whether a URL's data is cached.
        - Tracks how many times get_page is called.
        """
        rc.incr(f"count:{url}")
        
        # Check if the page is cached
        cached_content = rc.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode("utf-8")
        
        # Fetch the page if not cached
        response = fn(url)
        
        # Cache the page content with an expiration time of 10 seconds
        rc.setex(f"cached:{url}", 10, response)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """Makes an HTTP request to a given endpoint and returns the page content."""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'  # Replace with a reliable test URL
    content = get_page(url)
    print(content)
    content = get_page(url)
    print(content)
    access_count = rc.get(f"count:{url}")
    print(f"URL accessed {access_count.decode('utf-8')} times.")
