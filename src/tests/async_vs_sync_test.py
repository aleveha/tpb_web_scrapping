"""Test async vs sync data fetching"""

import time
from typing import List

import grequests
import requests

from shared import divide_to_chunks

# !!! Results can be different on different machines with different internet connection !!!

# SYNC 100:
# 100 = 17 sec

# ASYNC 100:
# 100 – 5 = 4 sec
# 100 – 10 = 2.35 sec
# 100 – 20 = 1.35 sec
# 100 – 30 = 1.18 sec
# 100 – 50 = 0.81 sec
# 100 – 100 = 0.72 sec

# RESULT 100:
# Array of 100 elements divided to smaller chunks of 20 elements fetched asynchronously
# is ~23.5 faster than array of 100 elements fetched synchronously


# SYNC 1000:
# 1000 = 174.85 sec

# ASYNC 1000:
# 1000 – 5 = 48.24 sec
# 1000 – 10 = 28.13 sec
# 1000 – 20 = 19.15 sec
# 1000 – 30 = 13.37 sec
# 1000 – 50 = 10.39 sec
# 1000 – 100 = 9.25 sec

# RESULT 1000:
# Array of 1000 elements divided to smaller chunks of 20 elements fetched asynchronously
# is ~23.5 faster than array of 100 elements fetched synchronously

URL = "https://www.google.com/"


def sync_fetching(urls: List[str]) -> None:
    """Fetch data synchronously"""
    start_time = time.perf_counter()

    for url in urls:
        requests.get(url)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Sync: {execution_time}\n")


def async_fetching(urls: List[str]) -> None:
    """Fetch data asynchronously"""
    for chunk_size in [5, 10, 20, 30, 50, 100]:
        chunked_array = list(divide_to_chunks(urls, chunk_size))

        start_time = time.perf_counter()

        for chunk in chunked_array:
            async_list = []
            for url in chunk:
                action_item = grequests.get(url)
                async_list.append(action_item)

            grequests.map(async_list)

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Async with chunk size ({chunk_size}): {execution_time}")


def response_hook(response, response_list, *args, **kwargs):
    """Response hook"""
    # Here you can do something with response and append it to response_list
    response_list.append(response.status_code)


def async_fetching_with_hook(urls: List[str]) -> None:
    """Fetch data asynchronously with hook"""
    chunk_size = 20
    chunked_array = list(divide_to_chunks(urls, chunk_size))

    for chunk in chunked_array:
        async_list = []
        response_list = []
        for url in chunk:
            action_item = grequests.get(url, hooks={"response": lambda res, *args, **kwargs: response_hook(res, response_list, args, kwargs)})
            async_list.append(action_item)

        grequests.map(async_list)
        print(f"Response list ({len(response_list)}): {response_list}")


def main():
    """Main function"""
    number = 100
    urls = [URL] * number
    print(f"URL: {URL}")
    print(f"Number of URLs: {number}")
    # sync_fetching(urls)
    # async_fetching(urls)
    async_fetching_with_hook(urls)


if __name__ == "__main__":
    main()
