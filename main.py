import multiprocessing
import time
import bz2
import os
import xml.sax
import re
from threading import Thread
import signal, sys
from exitbrake import ExitBrake

import database
from wikireader import WikiReader


def display(eb: ExitBrake, aq: multiprocessing.Queue, wq: multiprocessing, reader: WikiReader):
    before = 0

    while not eb.shutdown():
        print("Number of articles waiting to be processed: {0}".format(aq.qsize()))
        print("Number of processed articles waiting to be written: {0}".format(wq.qsize()))
        print("Number of article processed: {0}".format(reader.real_article_processed))
        print("Number of article skipped: {0}".format(reader.total_article_processed - reader.real_article_processed))
        print("Processing rate: " + str(reader.real_article_processed - before) + " articles/s")
        print("")

        before = reader.real_article_processed

        time.sleep(1)


def processArticle(eb: ExitBrake, aq: multiprocessing.Queue, wq: multiprocessing.Queue):
    while not eb.shutdown() or not aq.empty():
        page_title, page_text, redirect = aq.get()

        if redirect:
            wq.put((page_title, [page_text], True))
            continue

        # Begin text processing
        pages_mentioned = []

        # First remove nowiki tags (They can't be used as links)
        page_text = re.sub(r"<nowiki>(.*?)<\/nowiki>", "", page_text)

        # Find all possible links
        for match in re.finditer(r"\[\[(.*?)\]\]", page_text):
            # Remove wrapped brackets and
            # get "Page name" if the format is the following [[Page name | Displayed text]]
            link = page_text[match.start() + 2:match.end() - 2].split("|")[0]  # Remove the 2 brackets

            # Ignore external links
            if len(link) >= 7 and (link[0:6] == "http://" or link[0:6] == "https://"):
                continue

            # Get page name without section ( https://en.wikipedia.org/wiki/Help:Link#Section_linking_(anchors) )
            # [[Page name#Section name|displayed text]] <-- Another page
            # [[#Section name|displayed text]] <-- Same page

            if len(link) == 0: continue

            if link[0] == "#": continue  # Link to a section in the same page

            link = link.split("#")[0]

            pages_mentioned.append(link)

        wq.put((page_title, pages_mentioned, False))
    print("Done processing all article!")
    sys.exit() # Terminate "sub"-process


def writeToDatabase(eb: ExitBrake, wq: multiprocessing.Queue):
    db = database.connect()

    while not eb.shutdown() or not wq.empty():
        if wq.qsize() < 500 and not eb.shutdown():
            continue

        valid_article_batch = []
        redirect_batch = []

        while ((len(valid_article_batch) + len(redirect_batch)) < 500) and not wq.empty():
            page_title, mentioned_pages, redirect = wq.get()

            if redirect:
                redirect_batch.append((page_title, mentioned_pages[0]))
            else:
                valid_article_batch.append((page_title, mentioned_pages))

        try:
            print("Starting batch")

            # Insert valid article batch
            db.insertNewArticles(list(map(lambda x: x[0], valid_article_batch)), True)
            db.insertNewEdgesInArticlesLink(valid_article_batch)

            # Insert redirect article batch
            if len(redirect_batch) > 0:
                db.insertNewRedirects(redirect_batch)

            db.commit()
            print("Batch finished running")
        except Exception as error:
            print("Failed to write to database: {}".format(error))
            db.rollback()

    # Closing connection
    print("Closing db connection!!!")
    db.close()


def main():
    eb = ExitBrake()

    manager = multiprocessing.Manager()

    # This is a queue that can dequeue and enqueue items in different threads? (in a synchronized way)
    aq = manager.Queue(maxsize=1000)
    wq = manager.Queue(maxsize=4000)

    # Open the wiki dump
    wiki = bz2.BZ2File(os.environ.get("WIKI_XML_DUMP"))

    # Run x amount of processes that will do analysis on the texts of data
    processes = []
    for _ in range(1):
        pr = multiprocessing.Process(target=processArticle, args=(eb, aq, wq))
        processes.append(pr)
        pr.start()

    # Start thread that will write data to database
    write_th = Thread(target=writeToDatabase, args=(eb, wq))
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
        for p in processes:
            if p.is_alive():
                p.terminate()

        while True:
            if not write_th.is_alive() and not console_display_thread.is_alive():
                print("Bye bye!")
                sys.exit()
            time.sleep(1)

    signal.signal(signal.SIGINT, stopHandler)

    # Start reading the dumps
    xml.sax.parse(wiki, reader)
    print("Finished parsing the data! Terminating!")
    print("Waiting for article in queue to finish")

    eb.brake()

    # Wait for articles in queues to finish
    while True:
        time.sleep(1)
        should_end = False

        # Wait for all processes to finish
        for process in processes:
            if process.is_alive():
                should_end = True
                break
        if should_end:
            stopHandler(None, None)


if __name__ == "__main__":
    main()
