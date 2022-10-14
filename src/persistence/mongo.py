"""Mongo persistence"""
from typing import List

from pymongo import MongoClient

from typings import Article

client = MongoClient("mongodb://root:root@127.0.0.1:27017/")
tpb_db = client.get_database("tpb")

articles_collection = tpb_db.get_collection("articles")
links_collection = tpb_db.get_collection("links")


def insert_articles(new_articles: List[Article]) -> None:
    """Insert multiple articles to database"""
    articles_collection.insert_many([new_article.__dict__ for new_article in new_articles])


def article_exists(link: str) -> bool:
    """Check if article exists"""
    return bool(articles_collection.find_one({"link": link}))


def insert_links(links: List[str]) -> None:
    """Insert multiple links to database"""
    links_collection.insert_many([{"link": link} for link in links])


def get_links_by_slug(slug: str) -> List[str]:
    """Insert multiple links to database"""
    return [link["link"] for link in links_collection.find({"link": {"$regex": f"{slug}.*"}})]


def delete_link(link: str) -> None:
    """Delete link"""
    links_collection.delete_one({"link": link})


def main():
    """Main function"""
    # LINKS
    # delete all links
    # links_collection.delete_many({}})

    # get all links count
    print("Links ", links_collection.count_documents({}))

    # # # # #

    # ARTICLES
    # delete all articles
    # articles_collection.delete_many({})

    # get all articles count
    print("Articles ", articles_collection.count_documents({}))


if __name__ == "__main__":
    main()
