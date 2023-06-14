import time
import bz2
import os
import xml.sax
import re
from threading import Thread
from queue import Queue
import argparse
import sys
import database
import partition
from wikireader import WikiReader
import csv
from datetime import timedelta
from exitbrake import ExitBrake
from csvutils import csvFileObject, parseCSV


# This functions display current information about the processing of Wikipedia dumps
def display(reader: WikiReader, pq: Queue):
    starting_time = time.time()
    before_p = 0
    before_pq = 0
    print("")
    while True:
        pq_size = pq.qsize()
        time_elapsed = str(timedelta(seconds=(time.time() - starting_time)))
        print("\r{0}: pq size: {1}, a_processed: {2}, skipped: {3}, p_rate: {4} articles/s, pq_rate: {5} articles/s".format(
            time_elapsed,
            pq_size,
            reader.real_article_processed,
            reader.total_article_processed - reader.real_article_processed,
            reader.real_article_processed - before_p,
            before_pq - pq_size), end='')
        before_p = reader.real_article_processed
        before_pq = pq_size
        time.sleep(1)


# This function takes as a parameter the content of a wikipedia article and returns every articles title it mentions
def processArticle(page_text: str):
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

        pages_mentioned.append(link[0].upper() + link[1:])

    return pages_mentioned


# This (main) functions processes information the Wikipedia reader (WikiReader) has read
def writeToLocal(pq: Queue, eb: ExitBrake):
    article_csv, redirect_csv, pagesmentioned_csv = csvFileObject('w')

    article_w = csv.writer(article_csv, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
    redirect_w = csv.writer(redirect_csv, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
    pagesmentioned_w = csv.writer(pagesmentioned_csv, delimiter=' ', quoting=csv.QUOTE_MINIMAL)

    while not pq.empty() or not eb.shutdown():
        page_title, page_text, redirect = pq.get()

        if redirect:
            redirect_w.writerow([page_title, page_text])
        else:
            pages_mentioned = processArticle(page_text)
            article_w.writerow([page_title])
            pagesmentioned_w.writerows(map(lambda x: [page_title, x], pages_mentioned))
    print("closing")
    article_csv.close()
    redirect_csv.close()
    pagesmentioned_csv.close()


def dumpProcessing():
    # This is a queue that can dequeue and enqueue items in different threads? (in a synchronized way)
    pq = Queue(maxsize=2000)

    # Open the wiki dump
    wiki = bz2.BZ2File(os.environ.get("WIKI_XML_DUMP"))

    reader = WikiReader(lambda ns: ns == 0, pq.put)

    # Display how many pages has been analyzed
    eb = ExitBrake()
    console_display_thread = Thread(target=display, args=(reader, pq))
    console_display_thread.start()

    wlocal_thread = Thread(target=writeToLocal, args=(pq, eb))
    wlocal_thread.start()

    # Start reading the dumps
    xml.sax.parse(wiki, reader)
    print("\nFinished parsing the data! Terminating!")
    print("Waiting for article in queue to finish")


    # Wait for articles in queues to finish
    eb.brake()
    wlocal_thread.join()
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reformat_db", action="store_true")
    parser.add_argument("--csvtodb", action="store_true")
    parser.add_argument("--partition", action="store_true")
    args = parser.parse_args()

    if args.reformat_db:
        print("Reformating database")
        db = database.connect()
        try:
            db.reformatData()
            db.commit()
        except Exception as e:
            print("Failed to write to database: {}".format(e))
            db.rollback()
        db.close()
    elif args.csvtodb:
        parseCSV()
    elif args.partition:
        partition.performPartition()
    else:
        dumpProcessing()
