import sqlite3


class DatabaseHelper:
    def __init__(self, connection: sqlite3.Connection):
        self._cursor = connection.cursor()
        self.connection = connection

    def insertNewArticles(self, articles_title: list[str], visited: bool):
        query = "INSERT INTO article (title, visited) " \
                "VALUES (?, ?) ON CONFLICT(title) DO UPDATE set visited=1"

        self._cursor.executemany(query, list(map(lambda x: (x, visited), articles_title)))

    # Done in batches to increase db performance and not throttle write queue
    def insertNewEdgesInArticlesLink(self, data: list[tuple]):
        # Add unvisited articles
        # data = [(from, [article1, article 2]), (from, [article1, article2,...])]
        values_query1 = []
        values_query2 = []
        for edges in data:
            values_query1 += list(map(lambda x: (x, False), edges[1]))
            values_query2 += list(map(lambda x: (edges[0], x), edges[1]))

        query1 = "INSERT OR IGNORE INTO article (title, visited) VALUES (?, ?)"
        self._cursor.executemany(query1, values_query1)

        query2 = "INSERT OR IGNORE INTO article_link_edge_directed (from_article, to_article) " \
                 "VALUES (?, ?)"

        self._cursor.executemany(query2, values_query2)

    def insertNewRedirects(self, batch: list[tuple]):
        query = "INSERT INTO redirect (from_article, to_article) VALUES (?, ?)"
        self._cursor.executemany(query, batch)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()
