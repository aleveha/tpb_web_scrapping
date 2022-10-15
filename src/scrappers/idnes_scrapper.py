"""Parce www.idnes.cz"""
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from shared import scrap_web

URL = "https://www.idnes.cz/"


def sitemap_response_hook(response, response_list: List[str], base_url: str, *args, **kwargs) -> None:
    """Sitemap response hook"""
    soup = BeautifulSoup(response.text, "html.parser")
    res = [link.get("href") for link in soup.find_all("a", {"class": "art-link"}) if link.get("href").startswith(base_url)]
    response_list.extend(res)


def parse_html_article(html, url):
    """Parse HTML"""
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find("h1").text.replace("\xa0", " ").replace("\n", "")
    if title is None:
        raise Exception("Not found")

    article_content = soup.find("div", {"class": "bbtext"})
    content = "".join([p.text for p in article_content.find_all("p")]).replace("\xa0", " ").replace("\n", "").encode("utf-8", "ignore").decode("utf-8")
    publish_date = datetime.fromisoformat(soup.find("span", {"itemprop": "datePublished"}).get("content").replace("CET", "")).isoformat()

    comments_count = 0
    comments_block = soup.find("li", {"class": "community-discusion"})
    if comments_block:
        number = comments_block.find("a").find("span").text.split(" ")[0][1:-1]
        if number.isdigit():
            comments_count = int(number)

    category = url.replace(URL, "").split("/")[0]

    photos_count = len(article_content.find_all("img")) + 1
    return {
        "category": category,
        "comments_count": comments_count,
        "content": content,
        "link": url,
        "photos_count": photos_count,
        "publish_date": publish_date,
        "title": title,
    }


def main():
    """Main function"""
    print(f"Start scrapping {URL}")
    sitemap_links = [f"https://www.idnes.cz/zpravy/archiv{'' if i == 1 else f'/{i}'}?datum=&idostrova=idnes" for i in range(1, 10000)]
    scrap_web(sitemap_links, URL, sitemap_response_hook, parse_html_article)


if __name__ == "__main__":
    main()
