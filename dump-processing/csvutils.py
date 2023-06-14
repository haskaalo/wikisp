import csv
import os
import sys

import database
import time
from datetime import timedelta


# mode = w | r
def csvFileObject(mode: str):
    out_dir = os.environ.get('OUT_DIR')

    article_csv = open(os.path.join(out_dir, 'article.csv'), mode, newline='', encoding='utf-8')
    redirect_csv = open(os.path.join(out_dir, 'redirect.csv'), mode, newline='', encoding='utf-8')
    pagesmentioned_csv = open(os.path.join(out_dir, 'pagesmentioned.csv'), mode, newline='', encoding='utf-8')

    return article_csv, redirect_csv, pagesmentioned_csv


def writeArticleBatch(batch, visited, db: database.databasehelper.DatabaseHelper):
    try:
        db.insertNewArticles(batch, visited)
        db.commit()
        batch.clear()
    except Exception as error:
        print("Failed to write to database: {}".format(error))
        db.rollback()
        sys.exit()


def writeRedirectBatch(batch, db: database.databasehelper.DatabaseHelper):
    try:
        db.insertNewRedirects(batch)
        db.commit()
        batch.clear()
    except Exception as error:
        print("Failed to write to database: {}".format(error))
        db.rollback()
        sys.exit()


def writePagesMentionedBatch(batch, db: database.databasehelper.DatabaseHelper):
    try:
        db.insertNewEdgesInArticlesLink(batch)
        db.commit()
        batch.clear()
    except Exception as error:
        print("Failed to write to database: {}".format(error))
        db.rollback()
        sys.exit()


def parseCSV():
    starting_time = time.time()
    db = database.connect()
    article_csv, redirect_csv, pagesmentioned_csv = csvFileObject('r')

    #
    # First insert article titles from article.csv
    #
    print("Inserting article titles\n")
    article_r = csv.reader(article_csv, delimiter=' ', quoting=csv.QUOTE_MINIMAL)

    article_batch = []
    for i, row in enumerate(article_r):
        article_title = row[0]

        article_batch.append(article_title)
        print("\r{0}: Inserting article no. {1}".format(
            timedelta(seconds=(time.time() - starting_time)), i),
              end='')

        if len(article_batch) >= 500:
            writeArticleBatch(article_batch, True, db)

    if len(article_batch) > 0:
        writeArticleBatch(article_batch, True, db)

    #
    # Insert redirects
    #
    print("\nStarting inserting redirects...\n\n")
    redirect_r = csv.reader(redirect_csv, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
    redirect_batch = []

    for i, row in enumerate(redirect_r):
        print("\r{0}: Inserting redirect no. {1}".format(
            timedelta(seconds=(time.time() - starting_time)), i),
            end='')

        from_id = db.getArticleIDFromTitle(row[0])
        to_id = db.getArticleIDFromTitle(row[1])
        if from_id is None:
            from_id = db.insertNewArticle(row[0], False)
        if to_id is None:
            to_id = db.insertNewArticle(row[1], False)

        redirect_batch.append((from_id[0], to_id[0]))

        if len(redirect_batch) >= 500:
            writeRedirectBatch(redirect_batch, db)

    if len(redirect_batch) > 0:
        writeRedirectBatch(redirect_batch, db)

    #
    # Reformating redirects
    #
    # Starting reformating redirects
    print("Reformating redirects")
    try:
        db.reformatData()
        db.commit()
    except Exception as e:
        print("Failed to write to database: {}".format(e))
        db.rollback()
        return

    #
    # Insert article edges
    #
    print("Starting inserting article page mentionned...")
    pagesmentioned_r = csv.reader(pagesmentioned_csv, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
    pagesmentioned_batch = []

    for i, row in enumerate(pagesmentioned_r):
        print("\r{0}: Inserting page mentionned no. {1}".format(
            timedelta(seconds=(time.time() - starting_time)), i),
            end='')

        from_id = db.getArticleIDFromTitle(row[0])
        to_id = db.getArticleIDFromTitle(row[1])

        if from_id is None:
            print("Weirdly {0} is not in database".format(row[0]))
            return
        elif to_id is None:  # Mentioned page that doesn't exist or is not in a valid namespace
            continue

        pagesmentioned_batch.append((from_id[0], to_id[0]))

        if len(pagesmentioned_batch) >= 500:
            writePagesMentionedBatch(pagesmentioned_batch, db)

    if len(pagesmentioned_batch) > 0:
        writePagesMentionedBatch(pagesmentioned_batch, db)

    #
    # Create search article table
    #
    print("Creating search article table")
    try:
        db.createArticleTitleSearchTable()
        db.commit()
    except Exception as e:
        print("Failed to write to database: {}".format(e))
        db.rollback()
        return

    print("DONE!!!!!")
