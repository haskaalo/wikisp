package articlepath

import (
	"fanor.dev/wikisp/shortestpath/serializer"
	"fanor.dev/wikisp/shortestpath/utils"
)

type PredecessorMap map[int]int

func generatePredecessorPath(predecessor PredecessorMap, dest int) []int {
	var result []int

	for dest != -1 {
		// Add at index 0
		newResult := make([]int, len(result)+1)
		newResult[0] = dest
		copy(newResult[1:], result)

		result = newResult

		// next iteration
		dest = predecessor[dest]
	}

	return result
}

func ComputePathBFS(sourceID int, destinationID int, adjacencyList serializer.ArticleAdjacencyList) []int {
	bfsQueue := utils.InitQueue()
	predecessor := PredecessorMap{}

	bfsQueue.Enqueue(sourceID)
	predecessor[sourceID] = -1

	for !bfsQueue.IsEmpty() {
		articleID := bfsQueue.Dequeue()

		adjacentArticles := adjacencyList[articleID]

		for _, adjacentArticleID := range adjacentArticles {
			_, existVisitedArticle := predecessor[adjacentArticleID]
			if existVisitedArticle {
				continue
			}

			predecessor[adjacentArticleID] = articleID
			if adjacentArticleID == destinationID {
				return generatePredecessorPath(predecessor, adjacentArticleID)
			}

			bfsQueue.Enqueue(adjacentArticleID)
		}
	}

	return []int{}
}

func ExistPossiblePath(sourceID int, destinationID int, adjacencyList serializer.ComponentAdjacencyList) bool {
	bfsQueue := utils.InitQueue()
	visitedComponents := map[int]bool{}

	bfsQueue.Enqueue(sourceID)
	visitedComponents[sourceID] = true

	for !bfsQueue.IsEmpty() {
		componentID := bfsQueue.Dequeue()
		adjacentComponents := adjacencyList[componentID]

		for _, adjacentComponentID := range adjacentComponents {
			_, existVisitedComponents := visitedComponents[adjacentComponentID]
			if existVisitedComponents {
				continue
			}

			visitedComponents[adjacentComponentID] = true

			if adjacentComponentID == destinationID {
				return true
			}

			bfsQueue.Enqueue(adjacentComponentID)
		}
	}

	return false
}
