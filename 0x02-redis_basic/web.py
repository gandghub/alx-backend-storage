#!/usr/bin/env python3
"""
This module contains a function to cache web pages with an expiration time and track access counts.
"""
import redis
import requests
from typing import Callable
from functools import wraps

# Initialize the Redis client
r = redis.Redis()

def count_requests(method: Callable) -> Callable:
    """
    Decorator that tracks how many times a URL has been requested.
    
    Args:
        method: The method to be decorated.
    
    Returns:
        The decorated method.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function to count URL requests."""
        cache_key = f"count:{url}"
        r.incr(cache_key)  # Increment the count for this URL
        return method(url)
    return wrapper

@count_requests
def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a URL and caches it in Redis for 10 seconds.
    
    Args:
        url: The URL to retrieve.
    
    Returns:
        The HTML content of the URL.
    """
    # Check if the URL content is already cached
    cache_key = f"cached:{url}"
    cached_content = r.get(cache_key)
    if cached_content:
        return cached_content.decode('utf-8')

    # If not cached, fetch the content and cache it
    response = requests.get(url)
    html_content = response.text

    # Cache the content with an expiration time of 10 seconds
    r.setex(cache_key, 10, html_content)

    return html_content

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    
    # Fetch the page content
    print(get_page(url))
    
    # Fetch the page content again to demonstrate caching
    print(get_page(url))
    
    # Retrieve and print the access count for the URL
    count_key = f"count:{url}"
    print(f"URL accessed {r.get(count_key).decode('utf-8')} times.")
