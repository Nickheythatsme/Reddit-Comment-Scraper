import os
import sys
import threading
import time
import queue
import logging


class Write_comments:
    log = logging.getLogger("Write_comments")
    DATA_PATH = 'data/'
    NUMBER_WORKERS = 200

    def __init__(self, comments):
        self.comments = comments
        self.file_list = []
        self.threads = []
        self.lock = threading.Lock()
        self.comments_wrote = 0
        self.directory = Write_comments.DATA_PATH + str(comments[0].subreddit) + '/'
        self.queue = queue.Queue()

        self.read_dir()
        self.prep_queue()
        self.finish_queue()

    #Make the subreddit directory if it doesn't exist
    def make_dir(self):
        Write_comments.log.debug("Making and checking for directory")
        if not os.path.exists( self.directory ):
            return os.makedirs( self.directory )
        return True
    
    #Makes sure the directory exists and then reads the files from it
    def read_dir(self):
        self.make_dir()
        self.file_list = os.listdir(self.directory)
        Write_comments.log.info("Files loaded from {}: {}".format(self.directory, len(self.file_list)))
        return len(self.file_list)

    #Make the threads and prep the queue
    def prep_queue(self):
        Write_comments.log.debug("Preparing the queue")
        Write_comments.log.debug("Starting threads")
        for i in range(Write_comments.NUMBER_WORKERS):
            t = threading.Thread(target=self.writer)
            t.start()
            self.threads.append(t)
        Write_comments.log.debug("{} Threads started".format(len(self.threads)))
        Write_comments.log.debug("Filling queue")
        for comment in self.comments:
            self.queue.put(comment)
        return len(self.threads)
    
    #Clean up the queue. Stop workers and finish tasks
    def finish_queue(self):
        Write_comments.log.info("Waiting until all jobs are finished ({} job on {} threads)".format(
            self.queue.qsize(), len(self.threads)))
        #Block until all tasks are done
        self.queue.join()
        #Stop all workers
        Write_comments.log.debug("Stopping and joining writers")
        for i in range(Write_comments.NUMBER_WORKERS):
            self.queue.put(None)
        for t in self.threads:
            t.join()
        Write_comments.log.info("Comments written: {}".format(self.comments_wrote))
        return;

    #Takes one comment from the queue, then checks if it exists. If it doesn't we send it to the write function
    def writer( self ):
        while True:
            #Wait for the comment
            comment = self.queue.get()
            if comment is None:
                return;
            else:
                out_file = self.directory + str(comment.id)
            if comment.id in self.file_list:
                self.queue.task_done()
            else:
                self.increment_wrote()
                self.write( out_file, comment )
                self.queue.task_done()


    def increment_wrote(self, value=1):
        self.lock.acquire()
        try:
            self.comments_wrote += value
        except RunTimeError:
            Write_comments.log.warning("RunTimeError when incrementing comments_wrote {}")
        finally:
            self.lock.release()


    #Write one comment to the speicifed file
    def write( self, out_file, comment ):
        try:
            fout = open( out_file, 'w' )
            fout.write( str(comment.author) + '\n' +
                        str(comment.parent_id) + '\n' +
                        str(comment.submission.id) + '\n' + 
                        str(comment.created) + '\n' +
                        str(comment.score) + '\n' +
                        str(comment.body) )
            fout.close()
        except KeyboardInterrupt:
            fout.close()
            return False;
        return True;
