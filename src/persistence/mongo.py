"""Mongo persistence"""
from typing import List, Dict, Tuple

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


def get_all_articles_count() -> int:
    """Get all articles count"""
    return articles_collection.count_documents({})


def get_duplicates_count() -> int:
    """Get duplicates count"""
    return len(list(articles_collection.aggregate([{"$group": {"_id": "$link", "count": {"$sum": 1}}}, {"$match": {"count": {"$gt": 1}}}])))


def get_oldest_article_date() -> str:
    """Get oldest article date"""
    return articles_collection.find_one(sort=[("publish_date", 1)])["publish_date"]


def get_most_commented_article_title() -> Tuple[str, int]:
    """Get most commented article title"""
    article = articles_collection.find_one(sort=[("comments_count", -1)])
    return article["title"], article["comments_count"]


def get_article_with_most_photos_count() -> Tuple[str, int]:
    """Get article with most photos count"""
    article = articles_collection.find_one(sort=[("photos_count", -1)])
    return article["title"], article["photos_count"]


def get_articles_by_publish_year() -> List[Dict]:
    """Get articles by publish year"""
    return list(articles_collection.aggregate(
        [{"$group": {"_id": {"$year": {"$dateFromString": {"dateString": "$publish_date"}}}, "count": {"$sum": 1}}}, {"$sort": {"_id": 1}}])
    )


def get_unique_categories_count_with_articles_count() -> List[Dict]:
    """Get unique categories count with articles count"""
    return list(articles_collection.aggregate(
        [{"$group": {"_id": "$category", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])
    )


def get_most_frequent_words_in_title_by_specific_year(year: int = 2021, limit: int = 5) -> List[Dict]:
    """Get five most frequent words in title by specific year"""
    return list(articles_collection.aggregate([
        {"$match": {"publish_date": {"$regex": f"^{year}"}}},
        {"$project": {"title": {"$toLower": "$title"}, "title_words": {"$split": ["$title", " "]}}},
        {"$unwind": "$title_words"},
        {"$project": {"title_words": 1, "title_word_len": {"$strLenCP": "$title_words"}}},
        # {"$match": {"title_word_len": {"$gt": 3}}},
        {"$group": {"_id": "$title_words", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]))


def count_all_comments_in_all_articles() -> int:
    """Count all comments count"""
    return list(articles_collection.aggregate([{"$group": {"_id": None, "count": {"$sum": "$comments_count"}}}]))[0]["count"]


def count_all_words_in_content_in_all_articles():
    """Count all words count in all articles"""
    return list(articles_collection.aggregate([
        {"$project": {"content_words": {"$split": ["$content", " "]}}},
        {"$unwind": "$content_words"},
        {"$group": {"_id": "$_id", 'sum': {"$sum": 1}}},
        {"$group": {"_id": None, "count": {'$sum': '$sum'}}}
    ]))[0]["count"]


def get_most_frequent_words_in_content(limit: int = 8) -> List[Dict]:
    """Get most frequent words in content"""
    return list(articles_collection.aggregate([
        {"$project": {"content": {"$toLower": "$content"}, "content_words": {"$split": ["$content", " "]}}},
        {"$unwind": "$content_words"},
        {"$project": {"content_words": 1, "content_word_len": {"$strLenCP": "$content_words"}}},
        {"$match": {"content_word_len": {"$gt": 6}}},
        {"$group": {"_id": "$content_words", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]))


def get_articles_with_most_freq_specific_word_in_content(word: str, limit: int = 3) -> List[Dict]:
    """Get articles with most frequent specific word in content"""
    return list(articles_collection.aggregate([
        {"$match": {"content": {"$regex": f"{word}", "$options": "i"}}},
        {"$project": {"link": 1, "content": {"$toLower": "$content"}, "word_occur": {"$split": [f"$content", f"{word.lower()}"]}}},
        {"$unwind": "$word_occur"},
        {"$group": {"_id": "$link", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]))


def get_article_by_size(sorting: int = 1):
    """Get the smallest article"""
    return list(articles_collection.aggregate([
        {"$project": {"link": 1, "title": 1, "content_words": {"$split": ["$content", " "]}}},
        {"$unwind": "$content_words"},
        {"$group": {"_id": {"link": "$link", "title": "$title"}, 'article_size': {"$sum": 1}}},
        {"$sort": {"article_size": sorting}},
        {"$limit": 1}
    ]))[0]


def get_average_word_length_in_all_articles():
    """Get average word length in all articles"""
    return list(articles_collection.aggregate([
        {"$project": {"content_words": {"$split": ["$content", " "]}}},
        {"$unwind": "$content_words"},
        {"$project": {"content_word_len": {"$strLenCP": "$content_words"}}},
        {"$group": {"_id": None, "avg_word_len": {"$avg": "$content_word_len"}}}
    ]))[0]["avg_word_len"]


def get_months_with_most_and_least_articles(sorting: int = 1) -> Tuple[str, str]:
    """Get months with most and least articles"""
    return list(articles_collection.aggregate([
        {"$group": {"_id": {"$month": {"$dateFromString": {"dateString": "$publish_date"}}}, "count": {"$sum": 1}}},
        {"$sort": {"count": sorting}},
        {"$limit": 1}
    ]))[0]["_id"]


def get_articles_showing_addition_over_time() -> List[Dict]:
    """Get articles showing addition over time"""
    return list(articles_collection.aggregate([
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": {"$dateFromString": {"dateString": "$publish_date"}}}},
                    "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]))


def get_articles_content_count_and_comments_count() -> List[Dict]:
    """Get articles content count and comments count"""
    return list(articles_collection.aggregate([
        {"$project": {"_id": None, "content_words_count": 1, "comments_count": 1}},
    ]))


def get_articles_count_by_category() -> List[Dict]:
    """Get articles count by category"""
    return list(articles_collection.aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5000}}},
    ]))


def get_random_article() -> Dict:
    """Get random article"""
    return articles_collection.aggregate([{"$sample": {"size": 1}}]).next()


def get_avg_photos_count_in_articles() -> float:
    """Get average photos count in articles"""
    return list(articles_collection.aggregate([
        {"$group": {"_id": None, "avg_photos_count": {"$avg": "$photos_count"}}}
    ]))[0]["avg_photos_count"]


def get_articles_count_by_comments_count(comments_count: int) -> int:
    """Get articles count by comments count"""
    res = list(articles_collection.aggregate([
        {"$match": {"comments_count": {"$gt": comments_count}}},
        {"$group": {"_id": None, "count": {"$sum": 1}}}
    ]))
    return res[0]["count"] if len(res) > 0 else 0


def get_articles_count_per_category_by_year(year: int) -> List[Dict]:
    """Get articles count per category by year"""
    return list(articles_collection.aggregate([
        {"$match": {"publish_date": {"$regex": f"{year}", "$options": "i"}}},
        {"$group": {"_id": {"category": "$category", "year": {"$year": {"$dateFromString": {"dateString": "$publish_date"}}}},
                    "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]))


def get_articles_count_and_words_count() -> List[Dict]:
    """Get articles count and words count"""
    return list(articles_collection.aggregate([
        {"$project": {"_id": None, "content_words_count": 1, "comments_count": 1}},
    ]))


def get_average_word_length_in_article() -> List[Dict]:
    """Get average word length in article"""
    return list(articles_collection.aggregate([
        {"$project": {"_id": 1, "content_words": {"$split": ["$content", " "]}}},
        {"$unwind": "$content_words"},
        {"$project": {"_id": 1, "content_word_len": {"$strLenCP": "$content_words"}}},
        {"$group": {"_id": "$_id", "avg_word_len": {"$avg": "$content_word_len"}}},
        # {"$match": {"avg_word_len": {"$gt": 10}}},
    ]))


def get_articles_count_by_day_of_week() -> List[Dict]:
    """Get articles count by day of week"""
    return list(articles_collection.aggregate([
        {"$group": {"_id": {"$dayOfWeek": {"$dateFromString": {"dateString": "$publish_date"}}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]))


def get_articles_count_by_word_in_title_by_year(words: List[str]) -> List[Dict]:
    """Get articles count by word in title by year"""
    return list(articles_collection.aggregate([
        {"$match": {"title": {"$regex": f"({'|'.join(words)})", "$options": "i"}}},
        {"$group": {"_id": {"$year": {"$dateFromString": {"dateString": "$publish_date"}}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]))


def main():
    """Main function"""
    print("Articles count:", get_all_articles_count())


if __name__ == "__main__":
    main()
