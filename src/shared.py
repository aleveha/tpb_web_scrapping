"""Shared functions"""
from typing import List, Dict

import grequests
from bs4 import BeautifulSoup

from persistence.mongo import article_exists, insert_articles


def divide_to_chunks(array: List, chunk_size: int) -> List[List]:
    """Divide array to smaller chunks"""
    res = []
    for i in range(0, len(array), chunk_size):
        res.append(array[i:i + chunk_size])

    return res


def sitemap_response_hook(response, response_list: List[str], base_url: str, *args, **kwargs) -> None:
    """Sitemap response hook"""
    soup = BeautifulSoup(response.text, features="xml")
    sitemap_tags = soup.find_all("loc")
    response_list += [sitemap_tag.text for sitemap_tag in sitemap_tags if sitemap_tag.text != base_url and sitemap_tag.text.startswith(base_url)]


def load_links_chunk(request_link_chunk: List[str], base_url: str, response_hook) -> List[str]:
    """Load links"""
    requests = []
    links = []

    for link in request_link_chunk:
        if link not in [request.url for request in requests]:
            action_item = grequests.get(link, hooks={"response": lambda res, *args, **kwargs: response_hook(res, links, base_url, args, kwargs)})
            requests.append(action_item)

    grequests.map(requests)

    return list(set(links))


def load_articles_chunk(article_links_chunk: List[str], parse_html_article) -> None:
    requests = []
    response_list: List[Dict] = []

    for article_link in article_links_chunk:
        if article_exists(article_link):
            continue

        action_item = grequests.get(
            article_link,
            hooks={"response": lambda res, *args, **kwargs: article_response_hook(res, response_list, parse_html_article, args, kwargs)},
            timeout=2
        )
        requests.append(action_item)

    grequests.map(requests)

    if len(response_list) > 0:
        insert_articles(response_list)
        print(f"Inserted {len(response_list)} articles\n")


def article_response_hook(response, response_list: List[Dict], parse_html_article, *args, **kwargs) -> None:
    """Response hook"""
    try:
        article = parse_html_article(response.text, response.url)
        if article["content"] != "":
            response_list.append(article)

    except Exception as exc:
        print(f"Error: {exc}")


def scrap_web(request_links: List[str], base_url: str, parse_sitemap, parse_html_article) -> None:
    """Parse web"""
    links_chunk_size = 30
    links_chunk_size = len(request_links) if len(request_links) < links_chunk_size else links_chunk_size

    request_link_chunks = divide_to_chunks(request_links, links_chunk_size)

    for request_link_chunk in request_link_chunks:
        links = load_links_chunk(request_link_chunk, base_url, parse_sitemap)

        articles_chunk_size = 100
        articles_chunk_size = len(links) if len(links) < articles_chunk_size else articles_chunk_size

        chunked_article_links_array = divide_to_chunks(links, articles_chunk_size)

        for article_links_chunk_idx, article_links_chunk in enumerate(chunked_article_links_array):
            article_links_chunk_number = article_links_chunk_idx * articles_chunk_size
            print(f"Fetching {article_links_chunk_number + 1} – {article_links_chunk_number + articles_chunk_size}..")

            load_articles_chunk(article_links_chunk, parse_html_article)
