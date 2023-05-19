import sqlite3


class DatabaseHelper:
    def __init__(self, connection: sqlite3.Connection):
        self._cursor = connection.cursor()
        self.connection = connection

    def getAdjacentArticles(self, title: str) -> list[str]:
        query = """
            SELECT COALESCE(r.to_article, aled.to_article) FROM article_link_edge_directed aled
            LEFT JOIN redirect r ON aled.to_article=r.from_article
            WHERE aled.from_article=?"""

        self._cursor.execute(query, (title,))

        return list(map(lambda x: x[0], self._cursor.fetchall()))

    def getNumberArticles(self) -> int:
        query = "SELECT count(*) from article where visited=1"

        self._cursor.execute(query)

        return self._cursor.fetchone()[0]
