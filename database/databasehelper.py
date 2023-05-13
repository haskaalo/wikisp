import mysql.connector.cursor;
import mysql.connector.connection as mconnection;


class DatabaseHelper:
    def __init__(self, cursor: mysql.connector.cursor.MySQLCursor, connection: mconnection.MySQLConnection):
        self.cursor = cursor
        self.connection = connection

    def insertNewArticles(self, articles_title: list[str], visited: bool):
        query = "INSERT INTO article (title, visited) " \
                "VALUES (%s, %s) ON DUPLICATE KEY UPDATE visited=1"

        self.cursor.executemany(query, list(map(lambda x: (x, visited), articles_title)))

    def insertNewEdgesInArticleLink(self, from_article: str, to_articles: list[str]):
        # Add unvisited articles
        query1 = "INSERT IGNORE INTO article (title, visited) VALUES (%s, %s)"
        self.cursor.executemany(query1, list(map(lambda x: (x, False), to_articles)))

        query2 = "INSERT IGNORE INTO article_link_edge_directed (from_article, to_article) " \
                 "VALUES (%s, %s)"
        self.cursor.executemany(query2, list(map(lambda x: (from_article, x), to_articles)))

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()
