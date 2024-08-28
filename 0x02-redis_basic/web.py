#!/usr/bin/env python3
"""
Create a web cache.
"""
import redis
import requests
from typing import Optional

# Initialize the Redis client
rc = redis.Redis()


def get_page(url: str) -> str:
    """Get a page and cache the value."""
    # Check if the page is already cached
    cached_content: Optional[bytes] = rc.get(f"cached:{url}")
    if cached_content:
        return cached_content.decode("utf-8")

    # If not cached, fetch the content
    resp = requests.get(url)

    # Increment the URL access count
    rc.incr(f"count:{url}")

    # Cache the content with an expiration time of 10 seconds
    rc.setex(f"cached:{url}", 10, resp.text)

    return resp.text


if __name__ == "__main__":
    url = (
        'http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.exle.com'
    )
    content = get_page(url)
    print(content)

    # To demonstrate caching, fetching the page again should be fast
    content = get_page(url)
    print(content)

    # Print the access count
    access_count = rc.get(f"count:{url}")
    print(f"URL accessed {access_count.decode('utf-8')} times.")
