import multiprocessing
import queue
import time
import bz2
import os
import xml.sax
from threading import Thread
import signal, sys
from exitbrake import ExitBrake
import mysql.connector

import database
from wikireader import WikiReader


def display(eb: ExitBrake, aq: multiprocessing.Queue, wq: multiprocessing, reader: WikiReader):
    while True and not eb.shutdown():
        print("Number of articles waiting to be processed: {0}".format(aq.qsize()))
        print("Number of processed articles waiting to be written: {0}".format(wq.qsize()))
        print("Number of article processed: {0}".format(reader.real_article_processed))
        print("Number of article skipped: {0}".format(reader.total_article_processed - reader.real_article_processed))
        print("")

        #if reader.total_article_processed > 10000:
        #    print("Braking")
        #    eb.brake()

        time.sleep(1)


def processArticle(eb: ExitBrake, aq: multiprocessing.Queue, wq: multiprocessing.Queue):
    while not eb.shutdown() or not aq.empty():
        try:
            page_title, page_text = aq.get(block=False)
        except queue.Empty:
            continue

        # Ignore pages that are simply redirects (https://en.wikipedia.org/wiki/Help:Redirect
        if len(page_text) >= 9 and page_text[0:8] == "#REDIRECT":
            continue

        # Ignore external links
        if len(page_text) >= 7 and (page_text[0:6] == "http://" or page_text[0:6] == "https://"):
            continue

        # Begin text processing
        """openbracket_stack = []
        for i, c in enumerate(page_text):
            c = page_text[i]

            if c == "[" and i > 0 and c[i-1] != "\\":
                openbracket_stack.append("[")"""

        # Put the article data into a queue to get it wrote into database
        wq.put((page_title, []))


def writeToDatabase(eb: ExitBrake, wq: multiprocessing.Queue, db: database.databasehelper.DatabaseHelper):
    while not eb.shutdown() or not wq.empty():
        try:
            page_title, mentioned_pages = wq.get(block=False)
        except queue.Empty:
            continue

        try:
            db.insertNewArticle(page_title)

            for mentioned_page in mentioned_pages:
                db.insertNewEdgeInArticleLink(page_title, mentioned_page)
            db.commit()
        except mysql.connector.Error as error:
            print("Failed to write to database: {}".format(error))
            db.rollback()


def main():
    db = database.connect()

    eb = ExitBrake()

    manager = multiprocessing.Manager()

    # This is a queue that can dequeue and enqueue items in different threads? (in a synchronized way)
    aq = manager.Queue(maxsize=2000)
    wq = manager.Queue(maxsize=2000)

    # Open the wiki dump
    wiki = bz2.BZ2File(os.environ.get("WIKIGRAPHSTATS_XML_DUMP"))

    # Run x amount of processes that will do analysis on the texts of data
    processes = []
    for _ in range(6):
        pr = multiprocessing.Process(target=processArticle, args=(eb, aq, wq))
        processes.append(pr)
        pr.start()

    # Start thread that will write data to database
    write_th = Thread(target=writeToDatabase, args=(eb, wq, db))
    write_th.start()

    reader = WikiReader(lambda ns: ns == 0, aq.put)

    # Display how many pages has been analyzed
    console_display_thread = Thread(target=display, args=(eb, aq, wq, reader))
    console_display_thread.start()

    # Handle CTRL-C or sigint
    def stopHandler(sig, frame):
        # Signal that the app is about to close
        eb.brake()

        # Terminate article processing (doesn't matter if they were in the middle of doing something)
        for process in processes:
            process.terminate()

        while True:
            if not write_th.is_alive() and not console_display_thread.is_alive():
                sys.exit()

    signal.signal(signal.SIGINT, stopHandler)

    # Start reading the dumps
    xml.sax.parse(wiki, reader)
    print("Finished parsing the data!")

    stopHandler(None, None)


if __name__ == "__main__":
    main()
