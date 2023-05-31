import sqlite3


class DatabaseHelper:
    def __init__(self, connection: sqlite3.Connection):
        self._cursor = connection.cursor()
        self.connection = connection

    def insertNewArticles(self, articles_titles: list[str], visited: bool):
        query = "INSERT OR IGNORE INTO article (title, visited) " \
                "VALUES (?, ?)"

        self._cursor.executemany(query, list(map(lambda x: (x, visited), articles_titles)))

    def insertNewArticle(self, article_title: str, visited: bool):
        query = "INSERT INTO article (title, visited) " \
                "VALUES (?, ?) returning id"

        self._cursor.execute(query, (article_title, visited))

        return self._cursor.fetchone()

    def getArticleIDFromTitle(self, title: str):
        query = "SELECT id FROM article WHERE title=? LIMIT 1"

        self._cursor.execute(query, (title,))

        return self._cursor.fetchone()

    # Done in batches to increase db performance and not throttle write queue
    def insertNewEdgesInArticlesLink(self, data: list[(int, int)]):
        query = "INSERT OR IGNORE INTO article_link_edge_directed (from_article, to_article) " \
                 "VALUES (?, ?)"

        self._cursor.executemany(query, data)

    def insertNewRedirects(self, batch: list[tuple]):
        query = "INSERT OR IGNORE INTO redirect (from_article, to_article) VALUES (?, ?)"
        self._cursor.executemany(query, batch)

    def reformatData(self):
        # ===================================================
        # Fixes weirdly inverted redirects in wikipedia dumps
        # ===================================================

        print("REFORMAT: Starting fixing weirdly inverted redirects in wiki dumps")
        query = """
        select r.from_article, r.to_article from redirect r inner join article a on a.id=r.from_article and a.visited=1
        """

        self._cursor.execute(query)
        for toUpdate in self._cursor.fetchall():
            # Check if the inverted already exist
            self._cursor.execute("SELECT EXISTS(select * from redirect where from_article=?)", (toUpdate[1],))

            exist = self._cursor.fetchone()[0]

            if exist:  # right order already exists, therefore delete
                self._cursor.execute("DELETE FROM redirect WHERE from_article=?", (toUpdate[0],))
            else: # right order don't exist, so invert
                self._cursor.execute("""
                UPDATE redirect
                SET from_article = to_article, to_article = from_article
                WHERE from_article=?
                """, (toUpdate[0],))
                print("Inverted - from: " + str(toUpdate[0]) + " to:" + str(toUpdate[1]))
        print("REFORMAT: DONE Fixing weirdly inverted redirects in wiki dumps")

        # ===================================================
        # Delete false redirect loops in wikipedia dumps
        # ===================================================
        print("REFORMAT: Starting delete false redirect loops")
        query = """
        DELETE FROM redirect
        WHERE from_article IN (
            SELECT r.from_article as from_article from article a 
            inner join redirect r
            on r.from_article = a.id
            where a.visited=1
            and exists (select title, visited from article where id=r.to_article and visited=1)
        )
        """  # Deletes redirect rows where article are both visited, which means they aren't actual redirects

        self._cursor.execute(query)
        print("REFORMAT: DONE Delete false redirect loops")

        # ===================================================
        # Delete redirects that redirect to the same link (once) (from_article=to_article)
        # ===================================================
        print("REFORMAT: Starting deleting redirects where from_article=to_article")
        query = """
        DELETE FROM redirect WHERE from_article IN 
        (select from_article from redirect where from_article=to_article)"""
        self._cursor.execute(query)
        print("REFORMAT: DONE deleting redirects where from_article=to_article")

        # ==================================================
        # Deleting article that leads to nowhere
        # ==================================================
        print("REFORMAT: Starting deleting redirects that leads to nowhere")
        query = """
        WITH RECURSIVE cte(from_article, to_article, final_destination) AS (
        SELECT from_article, to_article, to_article as final_destination
        FROM redirect
        UNION ALL
        SELECT cte.from_article, redirect.to_article, redirect.to_article as final_destination
        FROM cte
        JOIN redirect ON cte.final_destination = redirect.from_article)
        SELECT from_article, final_destination
        FROM cte
        INNER JOIN article a on a.id=final_destination and a.visited=0
        """
        self._cursor.execute(query)

        redirects_to_del = self._cursor.fetchall()
        self._cursor.executemany("DELETE FROM article WHERE id=? OR id=? AND visited=0", redirects_to_del)
        print("REFORMAT: DONE deleting redirects that leads to nowhere")

        # ==================================================
        # Replacing all redirects with the final destination
        # ==================================================
        print("REFORMAT: Starting replacing all redirects with the final destination")

        query = """
        UPDATE redirect AS r
        SET to_article=ft.final_destination
        FROM (
                WITH RECURSIVE cte(from_article, to_article, final_destination) AS (
                SELECT from_article, to_article, to_article as final_destination
                FROM redirect
                UNION ALL
                SELECT cte.from_article, redirect.to_article, redirect.to_article as final_destination
                FROM cte
                JOIN redirect ON cte.final_destination = redirect.from_article
                )
                SELECT from_article, final_destination
                FROM cte
                WHERE final_destination NOT IN (select from_article from redirect)
        ) as ft
        WHERE r.from_article=ft.from_article
        """
        self._cursor.execute(query)

        print("REFORMAT: DONE replacing all redirects with the final destination")
        print("REFORMAT DONE!")

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()
