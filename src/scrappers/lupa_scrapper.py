"""Parce www.lupa.cz"""

from bs4 import BeautifulSoup

from shared import load_links, sitemap_response_hook, scrap_web

URL = "https://www.lupa.cz/clanky/"


def parse_html_article(html, _):
    """Parse HTML"""
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find("h1").text.replace("\xa0", " ").replace("\n", "")
    if title == "Článek nenalezen":
        raise Exception("Not found")

    category = soup.select('a[class*="design-label--default"]')[0].get("href").split("/")[-2]
    article_content = soup.select('div[class*="layout-article-content"]')[0]
    content = "".join([p.text for p in article_content.find_all("p")]).replace("\xa0", " ")
    publish_date = soup.select('span[class*="design-impressum__item-wrapper--date"]')[0] \
        .find("span", {"class": "design-impressum__item"}).text.replace("\xa0", " ").replace("\n", "")

    comments_count = 0
    comments_block = soup.find("span", {"class": "comments__number"})
    if comments_block:
        comments_count = int(comments_block.text)

    photos_count = len(article_content.find_all("img")) + 1
    return category, comments_count, content, photos_count, publish_date, title


def main():
    """Main function"""
    print(f"Start scrapping {URL}")
    sitemap_links = [f"https://www.lupa.cz/sitemap/sitemap_texts{'' if i == 0 else f'_{i}'}.xml" for i in range(0, 20)]
    links = load_links(sitemap_links, URL, sitemap_response_hook)
    scrap_web(links, parse_html_article)


if __name__ == "__main__":
    main()
