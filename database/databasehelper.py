import mysql.connector.cursor;
import mysql.connector.connection as mconnection;


class DatabaseHelper:
    def __init__(self, cursor: mysql.connector.cursor.MySQLCursor, connection: mconnection.MySQLConnection):
        self.cursor = cursor
        self.connection = connection

    def insertNewArticle(self, article_title: str):
        query = "INSERT IGNORE INTO article (title) VALUES (%s)"

        self.cursor.execute(query, (article_title,))

    def insertNewEdgeInArticleLink(self, from_title: str, to_title: str):
        query = "INSERT IGNORE INTO article_link_edge_directed (from_article, to_article) VALUES (%s, %s)"

        self.cursor.execute(query, (from_title, to_title))

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()
