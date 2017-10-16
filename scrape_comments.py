import sys
import praw
import logging
import time
import app_info 
from praw.models import MoreComments


class Scrape_comments:
    log = logging.getLogger("Scrape_comments")
    SUBMISSION_LIMIT = 20
    COMMENT_LIMIT = 25
    TIMEOUT = 5*60
    Reddit = praw.Reddit(client_id=app_info.client_id,
                         client_secret=app_info.client_secret,
                         password=app_info.password,
                         user_agent=app_info.user_agent,
                         username=app_info.username)

    def __init__(self, sub_name):
        self.sub_name = sub_name
        self.comments = []
        self.submissions = []

        self.get_subreddit()
        self.get_submission_comments()


    #Try to pull data from the subreddit 
    def get_subreddit( self ):
        try:
            for submission in Scrape_comments.Reddit.subreddit( self.sub_name ).hot(limit=Scrape_comments.SUBMISSION_LIMIT):
                self.submissions.append(submission)
        except praw.exceptions.APIException(error_type, message, field):
            Scrape_comments.log.warning("Sever side error: {}\n{}".format(error_type, message) )
            return error_type
        except praw.exceptions.CleintException(error_type, message, field):
            Scrape_comments.log.warning("Client side error: {}\n{}".format(error_type, message) )
            Scrape_comments.log.info("Got client side error. Waiting for {} minutes".format(Scrape_comments.TIMEOUT/60))
            time.sleep(Scrape_comments.TIMEOUT)
            return error_type
        except:
            e = sys.exc_info()[0]
            Scrape_comments.log.critial("Getting submission failed: unknown exception: {}".format(e))
            return None
        Scrape_comments.log.info("Pulled links from {}".format(self.sub_name))
        return len(self.submissions)


    #Get the comments from a submission. This recursively calls until there
    #are no more submission objects in the self.submissions list.
    def get_submission_comments( self ):
        if not self.submissions:
            Scrape_comments.log.info("Pulled {} comments from {}".format(len(self.comments),self.sub_name))
            return len(self.comments)
        submission = self.submissions.pop(0)
        submission.comments.replace_more(limit=0)
        Scrape_comments.log.info("Pulling comments from submission ID: {}".format(submission.fullname))
        comment_queue = submission.comments[:]
        while comment_queue:
            comment = comment_queue.pop(0)
            self.comments.append(comment)
        return self.get_submission_comments()


if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    scraper = Scrape_comments("pics")
    print("Comments scraped: {}".format(len(scraper.comments)))


