import database
from queue import Queue
import time

db = database.connectPartition()


def componentConnectsBatchWrite(batch: list[tuple]):

    try:
        db.addBatchComponentConnects(batch)
        db.commit()
        batch.clear()
    except Exception as error:
        print("Failed to write to database: {}".format(error))
        db.rollback()


def componentBatchWrite(batch: list[tuple]):
    try:
        db.addBatchComponentEdge(batch)
        db.commit()
        batch.clear()
    except Exception as error:
        print("Failed to write to database: {}".format(error))
        db.rollback()


def performBFS(component_id: int, starting_node: str):
    bfs_queue = Queue()
    comp_write_batch = []
    comp_connects_write_batch = []
    bfs_queue.put(starting_node)

    # value is distance from starting node
    visited_articles = {starting_node: 0}  # (256 bits * 10317320) in gb = ~0.33GB

    before_count_visited = 1  # For console logging

    while not bfs_queue.empty():
        if len(comp_write_batch) >= 500:
            componentBatchWrite(comp_write_batch)
        if len(comp_connects_write_batch) >= 100:
            componentConnectsBatchWrite(comp_connects_write_batch)

        article_id = bfs_queue.get()
        adj_articles = db.getAdjacentArticles(article_id)

        for adj_article_id in adj_articles:
            if adj_article_id in visited_articles:
                continue

            adj_article_level = visited_articles[article_id] + 1
            visited_articles[adj_article_id] = adj_article_level

            adj_article_component = db.getArticleComponentID(adj_article_id)
            if adj_article_component is not None:  # Has already been searched (by another bfs component search)
                comp_connects_write_batch.append((component_id, adj_article_component[0], article_id))
            else:
                bfs_queue.put(adj_article_id)
                comp_write_batch.append((component_id, adj_article_level, article_id, adj_article_id))

        print("\rGRAPH PARTITION: Visited nodes: " + str(len(visited_articles))
              + " bfs_queue_size: " + str(bfs_queue.qsize())
              + " article visited rate: "
              + str(len(visited_articles) - before_count_visited), end='')
        before_count_visited = len(visited_articles)

    # Cleanup queue
    if len(comp_write_batch) > 0:
        componentBatchWrite(comp_write_batch)

    if len(comp_connects_write_batch) > 0:
        componentConnectsBatchWrite(comp_connects_write_batch)


def performPartition():
    current_component_id = 0
    starting_node = db.getUnreachedArticle()

    while starting_node is not None:
        print("")
        print("GRAPH PARTITION: Current partition graph ID: " + str(current_component_id))
        print("")

        db.addArticleComponent((current_component_id, starting_node[0]))
        performBFS(current_component_id, starting_node[0])

        # Next iteration
        starting_node = db.getUnreachedArticle()
        current_component_id += 1

    print("Done partitioning the graph!")
    db.commit()
