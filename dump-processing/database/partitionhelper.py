import sqlite3


class PartitionDatabaseHelper:
    def __init__(self, connection: sqlite3.Connection):
        self._cursor = connection.cursor()
        self.connection = connection

    def getAdjacentArticles(self, article_id: str) -> list[str]:
        query = """
            SELECT COALESCE(r.to_article, aled.to_article) FROM article_link_edge_directed aled
            LEFT JOIN redirect r ON r.from_article=aled.to_article
            WHERE aled.from_article=?"""

        self._cursor.execute(query, (article_id,))

        return list(map(lambda x: x[0], self._cursor.fetchall()))

    def getNumberArticles(self) -> int:
        query = "SELECT count(*) from article where visited=1"

        self._cursor.execute(query)

        return self._cursor.fetchone()[0]

    def getUnreachedArticle(self):
        query = "SELECT id FROM article WHERE article.component_id IS NULL AND visited=1 LIMIT 1"

        self._cursor.execute(query)

        return self._cursor.fetchone()

    def getArticleComponentID(self, ID):
        query = "SELECT component_id FROM article WHERE id=? AND component_id IS NOT NULL AND visited=1"

        self._cursor.execute(query, (ID,))

        return self._cursor.fetchone()

    # batch = list[(component_id, level, predecessor, title)...]
    def addBatchComponentEdge(self, batch: list[tuple]):
        query = "UPDATE article SET component_id=?, component_level=?, predecessor=? WHERE id=?"

        self._cursor.executemany(query, batch)

    def addBatchComponentConnects(self, batch: list[tuple]):
        query = "INSERT INTO article_component_connects (component_id, connects_to_id, from_article) VALUES (?, ?, ?)"

        self._cursor.executemany(query, batch)

    def addArticleComponent(self, values: (int, int)):
        query = "INSERT INTO article_component (component_id, starting_article) values (?, ?)"

        self._cursor.execute(query, values)
        self.addBatchComponentEdge([(values[0], 0, None, values[1])])

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

