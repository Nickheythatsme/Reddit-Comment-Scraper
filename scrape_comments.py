import sys
import praw
import logging
import time
import app_info 
import threading
import queue
from praw.models import MoreComments


class Scrape_comments:
    log = logging.getLogger("Scrape_comments")
    SUBMISSION_LIMIT = 50
    TIMEOUT = 5*60
    MAX_THREADS = 2
    Reddit = praw.Reddit(client_id=app_info.client_id,
                         client_secret=app_info.client_secret,
                         password=app_info.password,
                         user_agent=app_info.user_agent,
                         username=app_info.username)

    def __init__(self, sub_name):
        self.sub_name = sub_name
        self.comments = []
        self.submissions = []
        self.threads = []
        self.comment_lock = threading.Lock()
        self.q = queue.Queue()

        self.get_subreddit()
        self.start_submission_download()


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


    def start_submission_download( self ):
        for i in range(Scrape_comments.MAX_THREADS):
            t = threading.Thread(target=self.get_submission_comments)
            self.threads.append(t)
            t.start()
        for submission in self.submissions:
            self.q.put(submission)
        self.q.join()
        for i in range(Scrape_comments.MAX_THREADS):
            self.q.put(None)
        for t in self.threads:
            t.join();
        Scrape_comments.log.info("Comments from {}: {}".format(self.sub_name, len(self.comments)))
        return len(self.comments)


    def add_comments(self, comments):
        self.comment_lock.acquire()
        try:
            for comment in comments:
                self.comments.append(comment)
        except RunTimeError:
            Scrape_comments.log.warning("RunTimeError when appending comments")
        finally:
            self.comment_lock.release()
        return True;


    def get_submission_comments( self ):
        comments = []
        while True:
            submission = self.q.get()
            if submission is None:
                return True
            submission.comments.replace_more(limit=0)
            comment_queue = submission.comments[:]
            while comment_queue:
                comment = comment_queue.pop(0)
                comments.append(comment)
                comment_queue.extend(comment.replies)
            self.add_comments( comments )
            Scrape_comments.log.debug("Number of comments from submission ID {}: {}".format(submission.fullname,len(comments)))
            comments.clear()
            self.q.task_done()
        return comments


if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    scraper = Scrape_comments("pics")
    print("Comments scraped: {}".format(len(scraper.comments)))


