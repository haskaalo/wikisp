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
    # data = [(from, [article1, article 2]), (from, [article1, article2,...])]
    def insertNewEdgesInArticlesLink(self, data: list[tuple]):
        # Add unvisited articles
        values_query1 = []
        values_query2 = []
        for edges in data:
            values_query1 += list(map(lambda x: (x, False), edges[1]))
            values_query2 += list(map(lambda x: (edges[0], x[0].upper() + x[1:]), edges[1]))

        query1 = "INSERT OR IGNORE INTO article (title, visited) VALUES (?, ?)"
        self._cursor.executemany(query1, values_query1)

        query2 = "INSERT OR IGNORE INTO article_link_edge_directed (from_article, to_article) " \
                 "VALUES (?, ?)"

        self._cursor.executemany(query2, values_query2)

    def insertNewRedirects(self, batch: list[tuple]):
        query = "INSERT INTO redirect (from_article, to_article) VALUES (?, ?)"
        self._cursor.executemany(query, batch)

    def reformatData(self):
        # ===================================================
        # Fixes weirdly inverted redirects in wikipedia dumps
        # ===================================================
        query1 = """
        select r.from_article, r.to_article from article a
    inner join redirect r
    on r.from_article = a.title
    where a.visited=1 and exists (select title, visited from article where title=r.to_article and visited=0);
        """

        self._cursor.execute(query1)
        for toUpdate in self._cursor.fetchall():
            # Check if the inverted already exist
            self._cursor.execute("SELECT EXISTS(select * from redirect where from_article=? and visited=1)", toUpdate[1])

            exist = self._cursor.fetchone()

            if exist:  # right order already exists, therefore delete
                self._cursor.execute("DELETE FROM redirect WHERE from_article=?", toUpdate[0])
            else: # right order don't exist, so invert
                self._cursor.execute("""
                UPDATE redirect
                SET from_article = to_article, to_article = from_article
                WHERE from_article=?
                """, toUpdate[0])
                print("Inverted - from: " + toUpdate[0] + " to:" + toUpdate[1])

        # ===================================================
        # Delete false redirect loops in wikipedia dumps
        # ===================================================
        query2 = """
        DELETE FROM redirect
        WHERE from_article IN (
            SELECT r.from_article as from_article from article a 
            inner join redirect r
            on r.from_article = a.title
            where a.visited=1
            and exists (select title, visited from article where title=r.to_article and visited=1)
        )
        """
        self._cursor.execute(query2)

        # ===================================================
        # Delete articles that don't exist (red link) or aren't in a valid namespace (Talk:, Help:, Wiki:, etc..)
        # ===================================================
        query3 = "PRAGMA foreign_keys = ON"
        self.connection.execute(query3) # Enable cascade effects
        cursor = self.connection.cursor()

        query4 = """
        DELETE FROM article AS a where a.visited = 0
        AND NOT EXISTS (
            select from_article from redirect r
            where from_article = upper(substr(a.title, 1, 1)) || substr(a.title, 2, length(a.title)))
        AND NOT EXISTS (
            select s.title from article s
            where s.title = upper(substr(a.title, 1, 1)) || substr(a.title, 2, length(a.title))
            and s.visited=1
        )
        """

        cursor.execute(query4)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()
