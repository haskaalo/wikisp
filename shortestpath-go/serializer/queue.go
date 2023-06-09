package serializer

type Queue struct {
	queue []int
}

func InitQueue() Queue {
	q := Queue{}
	q.queue = []int{}

	return q
}

func (q *Queue) Enqueue(item int) {
	q.queue = append(q.queue, item)
}

func (q *Queue) Dequeue() int {
	item := q.queue[0]
	q.queue = q.queue[1:]

	return item
}

func (q *Queue) IsEmpty() bool {
	return len(q.queue) == 0
}

func (q *Queue) Size() int {
	return len(q.queue)
}
