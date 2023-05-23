import queue
import sys
import threading

import database
import multiprocessing
from queue import Queue
import threading
import uuid


def end(bfs_queue, path_found):
    while not bfs_queue.empty():
        bfs_queue.get()
    path_found.set()


# multiprocessing value?
def bfs(dest: str, bfs_queue: Queue, visited_articles, predecessor, path_found: multiprocessing.Event, lock):
    db = database.connect()

    while not bfs_queue.empty():
        if path_found.is_set():
            end(bfs_queue, path_found)
            return

        while True:
            try:
                if path_found.is_set():
                    end(bfs_queue, path_found)
                    return

                article_title = bfs_queue.get(block=False)
                break
            except queue.Empty:
                continue

        adj_articles = db.getAdjacentArticles(article_title)

        for adjacent_article_title in adj_articles:
            with lock:
                if adjacent_article_title in visited_articles:
                    continue

            predecessor[adjacent_article_title] = article_title

            if adjacent_article_title == dest:
                print("FOUND!")
                end(bfs_queue, path_found)
                return

            with lock:
                visited_articles[adjacent_article_title] = visited_articles[article_title] + 1
            bfs_queue.put(adjacent_article_title)


class BFS:
    def __init__(self, source: str, dest: str):
        self.source = source
        self.dest = dest

    def printPath(self, dest, predecessor):
        if dest is None:
            return ""

        arrow = " -> "

        if predecessor[dest] is None:
            arrow = ""

        return self.printPath(predecessor[dest], predecessor) + arrow + dest

    def compute(self):
        # STEP 0 : Initialisation
        bfs_queue = Queue()
        bfs_queue.put(self.source)
        predecessor, visited_articles = {self.source: None}, {self.source: 0}

        path_found = threading.Event()

        num_process = 1
        lock = threading.RLock()
        threads = []

        #dest: str,
        # bfs_queue: Queue,
        # visited_articles,
        # predecessor,
        # path_found: multiprocessing.Event,
        # lock
        for _ in range(num_process):
            thread = threading.Thread(target=bfs, args=(self.dest, bfs_queue, visited_articles, predecessor, path_found, lock))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
            print("a process ended")

        lock.acquire()
        if path_found.is_set():
            return self.printPath(self.dest, predecessor)
        else:
            return None
