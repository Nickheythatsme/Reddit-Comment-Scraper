import sys
import logging
import time
import random
from write_comments import Write_comments
from scrape_comments import Scrape_comments

SUB_LIST = ["pics",
            "funny",
            "news",
            "politics",
            "theDonald",
            "gifs",
            "teenagers",
            "dataisbeautiful",
            "interestingasfuck",
            "nottheonion",
            "videos",
            "todayilearned",
            "LifeProTips",
            "WTF",
            "TumblrInAction",
            "gaming",
            "worldnews"]


def cycle( sub_name ):
    scraper = Scrape_comments( sub_name )
    writer = Write_comments(scraper.comments)


def main():
    random.seed(time.clock())
    random.shuffle(SUB_LIST)
    while True:
        for sub in SUB_LIST:
            logging.info("Starting cycle")
            cycle( sub )
            logging.info("Cycle finished, sleeping for 60 seconds")
            time.sleep(60)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

else:
    logging.basicConfig(level=logging.INFO)
    main()
