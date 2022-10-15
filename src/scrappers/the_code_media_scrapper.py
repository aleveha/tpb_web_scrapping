"""Parce www.thecode.media"""
from datetime import datetime
from random import randint
from typing import Dict

from bs4 import BeautifulSoup

from shared import scrap_web, sitemap_response_hook

URL = "https://thecode.media/"


def parse_html_article(html, url, fake_comments: bool = True) -> Dict:
    """Parse HTML"""
    soup = BeautifulSoup(html, 'html.parser')

    not_found = soup.find("div", {"class": "notFound__title"})
    if not_found is not None:
        raise Exception("Not found")

    title = soup.find("h1").text
    category = soup.find("a", {"rel": "category"}).text
    article_content = soup.find("div", {"class": "article-content"})
    content = "".join([p.text for p in article_content.find_all("p")]).replace("\xa0", " ")
    publish_date = datetime.strptime(soup.find("div", {"class": "post-date"}).text, "%d.%m.%Y").isoformat()
    comments_count = randint(0, 20) if fake_comments else len(soup.select('li[class*="CommentItem__Li"]'))
    photos_count = len(article_content.find_all("img")) + len(soup.find("div", {"class": "article-header"}).find_all("img"))

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
    sitemap_links = [f"https://thecode.media/post-sitemap{i}.xml" for i in range(1, 5)]
    scrap_web(sitemap_links, URL, sitemap_response_hook, parse_html_article)


if __name__ == "__main__":
    main()
