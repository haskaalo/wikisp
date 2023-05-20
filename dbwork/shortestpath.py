import database
import cachedict
import heapq

class ShortestPath:

    def __init__(self):
        self.db = database.connect()
        self.source = None
        self.dest = None
        self.marked_nodes = []
        self.marked_nodes_set = set()
        self.adj_articles_cache = cachedict.Cache()
        self.cache_hit = 0
        self.cache_missed = 0

    # TODO: Make this a function outside class to return an instance of this class like db
    def prepare(self, source: str, dest: str):
        self.source = source[0].upper() + source[1:]
        self.dest = dest[0].upper() + dest[1:]
        self.marked_nodes = []
        self.marked_nodes_set = set()
        self.adj_articles_cache = cachedict.Cache()
        self.cache_hit = 0
        self.cache_missed = 0

    def getAdjacentArticles(self, title):
        if self.adj_articles_cache.keyIn(title):
            self.cache_hit += 1
            adj_articles = self.adj_articles_cache.get(title)

        else:
            self.cache_missed += 1
            adj_articles = self.adjacentArticleNotMarked(title)
            self.adj_articles_cache.set(title, adj_articles)

        while len(adj_articles) > 0 and adj_articles[-1] in self.marked_nodes_set:
            adj_articles.pop(-1) # O(1) yay

        return adj_articles

    # Heap queue to prioritise based on distance
    def addMarkedNode(self, distance, title):
        heapq.heappush(self.marked_nodes, (distance, title))
        self.marked_nodes_set.add(title)

    # Dijkstra algorithm
    def compute(self):
        # STEP 0: INITIALISATION
        # This has a max size of (256 * len(select count(*) from article where visited=0)) bytes = approx 1GB
        self.addMarkedNode(0, self.source)
        unmarked_nodes_count = self.db.getNumberArticles()

        shortest_dist = {self.source: 0}  # key matches self.marked_node, value = distance between source and key
        predecessor = {self.source: None}

        while unmarked_nodes_count > 0:
            # STEP 1: In Dijkstra Find the shortest unmarked adjacent nodes for all marked nodes
            # But here all distance between nodes/vertexes = 1, so we just use the last one
            shortest_new_path = (None, None)

            for marked_node in self.marked_nodes:  # Prioritise nodes with low dist
                marked_node_title = marked_node[1]
                # TODO: TEST REMOVE AFTER
                if shortest_dist[marked_node_title] >= 3:
                    continue
                # TODO: END TEST

                # Avoid over reading database

                if shortest_new_path[0] is None:  # case 1: Initial
                    adj_articles = self.getAdjacentArticles(marked_node_title)

                    if len(adj_articles) == 0:
                        continue

                    shortest_adj_title = adj_articles[-1]
                    shortest_new_path = (marked_node_title, shortest_adj_title)
                else:
                    # previous: Previously/Current shortest path

                    possible_shortest_new_path_len = shortest_dist[marked_node_title] + 1
                    previous = shortest_dist[shortest_new_path[0]] + 1

                    if possible_shortest_new_path_len < previous:  # case 2
                        adj_articles = self.getAdjacentArticles(marked_node_title)

                        if len(adj_articles) == 0:
                            continue

                        shortest_adj_title = adj_articles[-1]  # since every distance of adj nodes = 1
                        shortest_new_path = (marked_node_title, shortest_adj_title)

            # STEP 2: Save new shortest path

            dist = shortest_dist[shortest_new_path[0]] + 1
            self.addMarkedNode(dist, shortest_new_path[1])
            shortest_dist[shortest_new_path[1]] = dist
            predecessor[shortest_new_path[1]] = shortest_new_path[0]

            toprint = ""
            n = shortest_new_path[1]
            while n is not None:
                toprint = n + " -> " + toprint
                n = predecessor[n]
            print(toprint)
            unmarked_nodes_count -= 1

            if shortest_new_path[1] == self.dest:
                return shortest_dist[shortest_new_path[1]]

    # Get all articles 1-click away from article title
    def adjacentArticleNotMarked(self, title: str):
        adjacent_articles = self.db.getAdjacentArticles(title)

        return list(filter(lambda a: a not in self.marked_nodes, adjacent_articles))
