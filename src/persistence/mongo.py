"""Mongo persistence"""
from typing import List, Dict

from pymongo import MongoClient

client = MongoClient("mongodb://root:root@127.0.0.1:27017/")
tpb_db = client.get_database("tpb")

articles_collection = tpb_db.get_collection("articles")


# export articles:
# mongoexport -d tpb -c articles -o articles.json --jsonArray --pretty --authenticationDatabase=admin -u root -p root
# docker cp mongo_tpb:"articles.json" ~/Personal/TUL/TPB/tpb_cviceni/articles.json


def insert_articles(new_articles: List[Dict]) -> None:
    """Insert multiple articles to database"""
    articles_collection.insert_many(new_articles)


def article_exists(link: str) -> bool:
    """Check if article exists"""
    return bool(articles_collection.find_one({"link": link}))


def main():
    """Main function"""
    # delete all articles
    # articles_collection.delete_many({})

    # get all articles count
    print("Articles ", articles_collection.count_documents({}))


if __name__ == "__main__":
    main()
