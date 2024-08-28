#!/usr/bin/env python3
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize the Redis client
rc = redis.Redis()


def cache_page(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(url: str) -> str:
        rc.incr(f"count:{url}")
        cached_content = rc.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode("utf-8")

        try:
            result = method(url)
            rc.setex(f"cached:{url}", 10, result)
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return "Error: Unable to fetch the URL."
    return wrapper


@cache_page
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = 'https://httpbin.org/delay/5'  # Replace with a reliable test URL
    content = get_page(url)
    print(content)
    content = get_page(url)
    print(content)
    access_count = rc.get(f"count:{url}")
    print(f"URL accessed {access_count.decode('utf-8')} times.")
