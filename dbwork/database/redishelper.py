import redis


class RedisHelper:

    def __init__(self, session_id: str):
        self.r = redis.Redis(host='localhost', port=6379)

        self.session_id = session_id
        self.va_name = session_id + ":" + "va"
        self.aa_name = session_id + ":" + "aa"

    def addVisitedArticle(self, article_name, distance):
        self.r.hset(self.va_name, article_name, distance)

    def getVisitedArticleDistance(self, key):
        return self.r.hget(self.va_name, key)

    def articleIsVisited(self, article):
        return self.getVisitedArticleDistance(article) is not None

    def addPredecessor(self, article_name, predecessor_name):
        self.r.hset(self.aa_name, article_name, predecessor_name)

    def getPredecessor(self, article_name):
        return self.r.hget(self.aa_name, article_name)

    def countVisited(self):
        return str(self.r.hlen(self.va_name))

    def cleanup(self):
        keys = self.r.keys(self.session_id + ":*")
        for key in keys:
            self.r.delete(key)

    def close(self):
        self.r.close()