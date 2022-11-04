"""Parse news"""
import time
from pprint import pprint

from graphs.graphs import main as plot_graphs
from persistence.mongo import get_all_articles_count, get_duplicates_count, get_oldest_article_date, get_most_commented_article_title, \
    get_article_with_most_photos_count, get_articles_by_publish_year, get_unique_categories_count_with_articles_count, \
    get_most_frequent_words_in_title_by_specific_year, count_all_comments_in_all_articles, count_all_words_in_content_in_all_articles, \
    get_most_frequent_words_in_content, get_articles_with_most_freq_specific_word_in_content, get_article_by_size, \
    get_average_word_length_in_all_articles, get_months_with_most_and_least_articles, get_articles_count_per_category_by_year, get_random_article, \
    get_avg_photos_count_in_articles, get_articles_count_by_comments_count
from scrappers.idnes_scrapper import main as idnes_scrapper
from scrappers.lupa_scrapper import main as lupa_scrapper
from scrappers.the_code_media_scrapper import main as the_code_media_scrapper


def load_data():
    """Load data"""
    scrappers = [the_code_media_scrapper, lupa_scrapper, idnes_scrapper]

    all_start_time = time.perf_counter()

    for scrapper_idx, scrapper in enumerate(scrappers):
        print(f"Scrapper {scrapper_idx + 1}/{len(scrappers)}\n")

        start_time = time.perf_counter()

        scrapper()

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Finish with time: {execution_time}s\n\n")

    all_end_time = time.perf_counter()
    all_execution_time = all_end_time - all_start_time
    print(f"Finish all scrappers with time: {all_execution_time}s")


def get_basic_info():
    """Get basic info"""
    print("1. Articles count:", get_all_articles_count())
    print("2. Duplicates count:", get_duplicates_count())
    print("3. Oldest article date:", get_oldest_article_date())
    print("4. Most commented article: ", get_most_commented_article_title())
    print("5. Article with most photos: ", get_article_with_most_photos_count())
    print("6. Articles by publish year:")
    pprint(get_articles_by_publish_year())
    print("7. Unique categories count with articles count:")
    pprint(get_unique_categories_count_with_articles_count())
    print("8. Five most freq words in specific year:")
    pprint(get_most_frequent_words_in_title_by_specific_year())
    print("9. Count all comments count: ", count_all_comments_in_all_articles())
    print("10. Count all words count: ", count_all_words_in_content_in_all_articles())

    print("11. Eight most freq words in content:")
    pprint(get_most_frequent_words_in_content())
    print("12. Articles with most freq specific word in content:")
    pprint(get_articles_with_most_freq_specific_word_in_content("covid"))
    print("13.1 Smallest article:")
    pprint(get_article_by_size(1))
    print("13.2 Biggest article:")
    pprint(get_article_by_size(-1))
    print("14. Average word length in all articles: ", get_average_word_length_in_all_articles())
    print("15.1 Months with least articles:", get_months_with_most_and_least_articles(1))
    print("15.2 Months with most articles:", get_months_with_most_and_least_articles(-1))


def get_more_info():
    """Get more info"""
    print("16. Get random article:")
    pprint(get_random_article())
    print("17. Articles count:", get_all_articles_count())
    print("18. Avg photo count per article:", get_avg_photos_count_in_articles())
    print("19. More than 100 comments at article count:", get_articles_count_by_comments_count(100))
    print("20. Articles count per category at 2022 year:")
    pprint(get_articles_count_per_category_by_year(2022))


def main():
    """Main function"""
    load_data()
    get_basic_info()
    plot_graphs()
    get_more_info()


if __name__ == "__main__":
    main()
