package articlepath

import "fanor.dev/wikisp/shortestpath/serializer/database"

type ArticleQueue struct {
	queue []database.AdjacentArticle
}

func InitArticleQueue() ArticleQueue {
	q := ArticleQueue{}
	q.queue = []database.AdjacentArticle{}
	return q
}

func (q *ArticleQueue) Enqueue(item database.AdjacentArticle) {
	q.queue = append(q.queue, item)
}

func (q *ArticleQueue) Dequeue() database.AdjacentArticle {
	item := q.queue[0]
	q.queue = q.queue[1:]
	return item
}

func (q *ArticleQueue) IsEmpty() bool {
	return len(q.queue) == 0
}

func (q *ArticleQueue) Size() int {
	return len(q.queue)
}
