"""Shared functions"""
from typing import List

import grequests
from bs4 import BeautifulSoup

from persistence.mongo import delete_link, get_links_by_slug, insert_links, article_exists, insert_articles
from typings import Article


def divide_to_chunks(array: List, chunk_size: int) -> List[List]:
    """Divide array to smaller chunks"""
    res = []

    for i in range(0, len(array), chunk_size):
        res.append(array[i:i + chunk_size])

    return res


def remove_duplicates(array: List) -> List:
    """Remove duplicates from string array"""
    without_duplicates = []

    for elem in array:
        if elem not in without_duplicates:
            without_duplicates.append(elem)
            continue

    return without_duplicates


def sitemap_response_hook(response, response_list: List[str], base_url: str, *args, **kwargs) -> None:
    """Sitemap response hook"""
    soup = BeautifulSoup(response.text, features="xml")
    sitemap_tags = soup.find_all("loc")
    response_list += [sitemap_tag.text for sitemap_tag in sitemap_tags if sitemap_tag.text != base_url and sitemap_tag.text.startswith(base_url)]


def load_links(request_links: List[str], base_url: str, response_hook) -> List[str]:
    """Load links"""
    print("Loading links..")

    exists_links = get_links_by_slug(base_url)

    if len(exists_links) > 0:
        return exists_links

    chunk_size = 30
    actual_chunk_size = len(request_links) if len(request_links) < chunk_size else chunk_size
    request_link_chunks = divide_to_chunks(request_links, actual_chunk_size)
    response_list = []

    for request_link_chunk in request_link_chunks:
        async_list = []
        links = []

        for link in request_link_chunk:
            if link in response_list:
                continue

            action_item = grequests.get(link, hooks={"response": lambda res, *args, **kwargs: response_hook(res, links, base_url, args, kwargs)})
            async_list.append(action_item)

        grequests.map(async_list)

        links, duplicates = remove_duplicates(links)

        print(f"Inserting {len(links)} links..")
        insert_links(links)
        response_list += links

    return response_list


def article_response_hook(response, response_list: List[Article], parse_html_article, *args, **kwargs) -> None:
    """Response hook"""
    try:
        category, comments_count, content, photos_count, publish_date, title = parse_html_article(response.text, response.url)
        if content == "":
            print(f"Empty content, delete and skip: {response.url}")
            delete_link(response.url)
            return
        response_list.append(Article(category, comments_count, content, response.url, photos_count, publish_date, title))
    except Exception as exc:
        print(f"Error: {exc}")
        print(f"Delete and skip: {response.url}")
        delete_link(response.url)


def scrap_web(links: List[str], parse_html_article) -> None:
    """Parse web"""
    print(f"\nStart scrapping {len(links)} links..\n")
    chunk_size = 50
    chunked_links_array = list(divide_to_chunks(links, chunk_size))
    inserted_articles_count = 0
    for chunk_idx, links_chunk in enumerate(chunked_links_array):
        chunk_number = chunk_idx * chunk_size
        print(f"Fetching {chunk_number + 1} – {chunk_number + chunk_size}..")

        async_list = []
        response_list: List[Article] = []
        for link_idx, link in enumerate(links_chunk):
            if article_exists(link):
                continue
            action_item = grequests.get(
                link,
                hooks={"response": lambda res, *args, **kwargs: article_response_hook(res, response_list, parse_html_article, args, kwargs)},
                timeout=2
            )
            async_list.append(action_item)

        grequests.map(async_list)
        if len(response_list) > 0:
            insert_articles(response_list)
            inserted_articles_count += len(response_list)
            print(f"Inserted {len(response_list)} articles\n")

    print(f"Inserted {inserted_articles_count}/{len(links)} articles")
