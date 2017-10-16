import os
import sys
import praw
import logging
import time
from write_comments import Write_comments
from scrape_comments import Scrape_comments

SUBMISSION_LIMIT = 10

SUB_LIST = ["pics","funny","news","politics","theDonald","gifs","teenagers"]



def cycle( sub_name ):
    scraper = Scrape_comments( sub_name )
    writer = Write_comments(scraper.comments)


def main():
    while True:
        for sub in SUB_LIST:
            logging.debug("Starting cycle")
            cycle( sub )
            logging.debug("Cycle finished, sleeping for 60 seconds")
            time.sleep(60)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()

else:
    main()
