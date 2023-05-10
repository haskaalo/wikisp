import multiprocessing
import time
import bz2
import os
import xml.sax
from threading import Thread
from typing import Optional

import mysql.connector

import database
from wikireader import WikiReader

shutdown = False


def display(aq: multiprocessing.Queue, wq: multiprocessing, reader: WikiReader):
    while True and not shutdown:
        print("Number of articles waiting to be processed: {0}".format(aq.qsize()))
        print("Number of processed articles waiting to be written: {0}".format(wq.qsize()))
        print("Number of article processed: {0}".format(reader.real_article_processed))
        print("Number of article skipped: {0}".format(reader.total_article_processed - reader.real_article_processed))
        print("")
        time.sleep(1)


def processArticle(aq: multiprocessing.Queue, wq: multiprocessing):
    while not shutdown or not aq.empty():
        page_title, page_text = aq.get()

        # TODO: Do the processing here

        # Put the article data into a queue to get it wrote into database
        wq.put((page_title, []))


def writeToDatabase(wq: multiprocessing, db: database.databasehelper.DatabaseHelper):
    while not shutdown or not wq.empty():
        page_title, mentioned_pages = wq.get()

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

    manager = multiprocessing.Manager()

    # This is a queue that can dequeue and enqueue items in different threads? (in a synchronized way)
    aq = manager.Queue(maxsize=2000)
    wq = manager.Queue(maxsize=2000)

    # Open the wiki dump
    wiki = bz2.BZ2File(os.environ.get("WIKIGRAPHSTATS_XML_DUMP"))

    # Run x amount of processes that will do analysis on the texts of data
    processes = []
    for _ in range(15):
        pr = multiprocessing.Process(target=processArticle, args=(aq, wq))
        processes.append(pr)
        pr.start()

    # Start thread that will write data to database
    write_th = Thread(target=writeToDatabase, args=(wq, db))
    write_th.start()


    global reader
    reader = WikiReader(lambda ns: ns == 0, aq.put)

    # Display how many pages has been analyzed
    console_display_thread = Thread(target=display, args=(aq, wq, reader))
    console_display_thread.start()

    # Start reading the dumps
    xml.sax.parse(wiki, reader)

    global shutdown
    shutdown = True


if __name__ == "__main__":
    main()
