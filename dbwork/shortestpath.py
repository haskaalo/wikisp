import database
import cachedict

class ShortestPath:

    def __init__(self):
        self.db = database.connect()
        self.source = None
        self.dest = None
        self.marked_nodes = set()
        self.adj_articles_cache = cachedict.Cache()

    # TODO: Make this a function outside class to return an instance of this class like db
    def prepare(self, source: str, dest: str):
        self.source = source[0].upper() + source[1:]
        self.dest = dest[0].upper() + dest[1:]
        self.marked_nodes = set()
        self.adj_articles_cache = cachedict.Cache()

    def getAdjacentArticles(self, title):
        if self.adj_articles_cache.keyIn(title):
            adj_articles = self.adj_articles_cache.get(title)

            if len(adj_articles) > 0:
                adj_articles.pop(0)  # All distances = 1

            return adj_articles
        else:
            adj_articles = self.adjacentArticleNotMarked(title)
            self.adj_articles_cache.set(title, adj_articles)

            return adj_articles

    # Dijkstra algorithm
    # TODO: Try to do it using BFS? Since a property of BFS is the link between a node and another one is garanteed to be minimal in terms of edges to search
    def compute(self):
        # STEP 0: INITIALISATION
        # This has a max size of (256 * len(select count(*) from article where visited=0)) bytes = approx 1GB
        self.marked_nodes.add(self.source)  # Init
        unmarked_nodes_count = self.db.getNumberArticles()
        shortest_dist = dict()  # key matches self.marked_node, value = distance between source and key
        shortest_dist[self.source] = 0

        while unmarked_nodes_count > 0:
            # STEP 1: In Dijkstra Find the shortest unmarked adjacent nodes for all marked nodes
            # But here all distance between nodes/vertexes = 1, so we just use the first one
            shortest_new_path = (None, None)  # min

            for marked_node_title in self.marked_nodes:
                # TODO: TEST REMOVE AFTER
                if shortest_dist[marked_node_title] >= 2:
                    continue
                # TODO: END TEST

                # Avoid over reading database

                if shortest_new_path[0] is None:  # case 1: Initial
                    adj_articles = self.getAdjacentArticles(marked_node_title)
                    if len(adj_articles) == 0: continue

                    shortest_adj_title = adj_articles[0]
                    shortest_new_path = (marked_node_title, shortest_adj_title)
                else:
                    # previous: Previously/Current shortest path

                    possible_shortest_new_path_len = shortest_dist[marked_node_title] + 1
                    previous = shortest_dist[shortest_new_path[0]] + 1

                    if possible_shortest_new_path_len < previous:  # case 2
                        adj_articles = self.getAdjacentArticles(marked_node_title)
                        if len(adj_articles) == 0: continue

                        shortest_adj_title = adj_articles[0]  # since every distance of adj nodes = 1
                        shortest_new_path = (marked_node_title, shortest_adj_title)

            # STEP 2: Save new shortest path
            print(shortest_new_path[1])

            self.marked_nodes.add(shortest_new_path[1])
            shortest_dist[shortest_new_path[1]] = shortest_dist[shortest_new_path[0]] + 1
            unmarked_nodes_count -= 1

            if shortest_new_path[1] == self.dest:
                return shortest_dist[shortest_new_path[1]]

    # Get all articles 1-click away from article title
    def adjacentArticleNotMarked(self, title: str):
        adjacent_articles = self.db.getAdjacentArticles(title)

        return list(filter(lambda a: a not in self.marked_nodes, adjacent_articles))
