from matplotlib import pyplot

from persistence.mongo import get_articles_showing_addition_over_time, get_articles_content_count_and_comments_count, get_articles_count_by_category, \
    get_average_word_length_in_article, get_articles_count_by_day_of_week, get_articles_count_by_word_in_title_by_year


# draw a curve showing the addition of articles over time
def plot_articles_count_by_date() -> None:
    """Plot articles count by date"""
    articles_count_by_date = get_articles_showing_addition_over_time()

    all_articles_count = 0
    for article in articles_count_by_date:
        all_articles_count += article["count"]
        article["count"] = all_articles_count

    pyplot.plot([article["_id"] for article in articles_count_by_date], [article["count"] for article in articles_count_by_date])
    pyplot.show()


# draw a bar chart showing the number of articles in each year
def plot_articles_count_by_year() -> None:
    """Plot articles count by year"""
    articles_count_by_year = get_articles_showing_addition_over_time()
    pyplot.bar([article["_id"].split("-")[0] for article in articles_count_by_year], [article["count"] for article in articles_count_by_year])
    pyplot.show()


# draw a scatter plot showing the relationship between the length of the cell and the number of comments
def plot_article_size_vs_comments_count() -> None:
    """Plot article size vs comments count"""
    articles = get_articles_content_count_and_comments_count()
    pyplot.scatter([article["content_words_count"] for article in articles], [article["comments_count"] for article in articles])
    pyplot.show()


# draw a pie chart showing the proportion of articles in each category
def plot_articles_count_by_category() -> None:
    """Plot articles count by category"""
    articles_count_by_category = get_articles_count_by_category()
    pyplot.pie([article["count"] for article in articles_count_by_category], labels=[article["_id"] for article in articles_count_by_category])
    pyplot.show()


# draw a histogram for the number of words in the articles
def plot_articles_count_by_word_count() -> None:
    """Plot articles count by word count"""
    articles_count_by_word_count = get_articles_content_count_and_comments_count()
    pyplot.hist([article["content_words_count"] for article in articles_count_by_word_count])
    # pyplot.hist([article["content_words_count"] for article in articles_count_by_word_count if article["content_words_count"] > 5000])
    pyplot.show()


# draw a histogram for avg words length in the articles
def plot_articles_avg_word_length() -> None:
    """Plot articles avg word length"""
    articles_avg_word_length = get_average_word_length_in_article()
    pyplot.hist([article["avg_word_len"] for article in articles_avg_word_length])
    pyplot.show()


# draw a timeline showing the occurrence of the word coronavirus in the title of the articles
def plot_articles_count_by_word_in_title() -> None:
    """Plot articles count by word in title"""
    articles_count_by_word_in_title_1 = get_articles_count_by_word_in_title_by_year(["koronavirus", "covid"])
    articles_count_by_word_in_title_2 = get_articles_count_by_word_in_title_by_year(["vakc", "vaccine"])
    print(articles_count_by_word_in_title_1)
    print(articles_count_by_word_in_title_2)
    pyplot.plot([article["_id"] for article in articles_count_by_word_in_title_1],
                [article["count"] for article in articles_count_by_word_in_title_1])
    pyplot.plot([article["_id"] for article in articles_count_by_word_in_title_2],
                [article["count"] for article in articles_count_by_word_in_title_2])
    pyplot.show()


# plot a histogram for the number of articles on each day of the week
def plot_articles_count_by_day_of_week() -> None:
    """Plot articles count by day of week"""
    articles_count_by_day_of_week = get_articles_count_by_day_of_week()
    pyplot.hist([article["_id"] for article in articles_count_by_day_of_week],
                weights=[article["count"] for article in articles_count_by_day_of_week])
    pyplot.show()


def main():
    """Main function"""
    plot_articles_count_by_date()
    plot_articles_count_by_year()
    plot_article_size_vs_comments_count()
    plot_articles_count_by_category()
    plot_articles_count_by_word_count()
    plot_articles_avg_word_length()
    plot_articles_count_by_day_of_week()
    plot_articles_count_by_word_in_title()


if __name__ == '__main__':
    main()
