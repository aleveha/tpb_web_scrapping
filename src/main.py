"""Parse news"""
import time

from scrappers.idnes_scrapper import main as idnes_scrapper
from scrappers.lupa_scrapper import main as lupa_scrapper
from scrappers.the_code_media_scrapper import main as the_code_media_scrapper


def main():
    """Main function"""
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


if __name__ == "__main__":
    main()
