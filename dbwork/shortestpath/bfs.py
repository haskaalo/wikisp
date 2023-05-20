from queue import Queue
import database


class BFS:
    def __init__(self, source: str, dest: str):
        self.db = database.connect()
        self.source = source
        self.dest = dest
        self.bfs_queue = Queue()
        self.visited_articles = {}

    def printPath(self, dest, predecessor):
        if dest is None:
            return ""

        arrow = " -> "
        if predecessor[dest] == None:
            arrow = ""

        return dest + arrow + self.printPath(predecessor[dest], predecessor)

    def compute(self):
        # STEP 0: Initialisation
        predecessor = {self.source: None}
        self.bfs_queue.put(self.source)
        self.visited_articles[self.source] = 0

        found = False
        count = 0
        while not self.bfs_queue.empty():
            count += 1
            article_title = self.bfs_queue.get()
            print("\rCurrent level: " + str(self.visited_articles[article_title]) +
                  " and processed: " + str(count)
                  + " number of articles in queue: " + str(self.bfs_queue.qsize()), end='')
            adj_articles = self.db.getAdjacentArticles(article_title)

            for adjacent_article_title in adj_articles:
                if adjacent_article_title in self.visited_articles:
                    continue
                elif adjacent_article_title == self.dest:
                    found = True

                predecessor[adjacent_article_title] = article_title
                self.bfs_queue.put(adjacent_article_title)
                self.visited_articles[adjacent_article_title] = self.visited_articles[article_title] + 1

            if found:
                break

        if found is True:
            return self.printPath(self.dest, predecessor)
        else:
            return None
