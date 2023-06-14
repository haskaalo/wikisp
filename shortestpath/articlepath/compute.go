package articlepath

import (
	"github.com/haskaalo/wikisp/serializer"
	"github.com/haskaalo/wikisp/utils"
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

func getRealID(source int, redirectMap serializer.RedirectMap) int {
	val, exist := redirectMap[source]
	if !exist {
		return source
	}

	return val
}

func ComputePathBFS(sourceID int, destinationID int, adjacencyList serializer.ArticleAdjacencyList, redirectMap serializer.RedirectMap) []int {
	bfsQueue := utils.InitQueue()
	predecessor := PredecessorMap{}
	visitedArticles := map[int]bool{}

	bfsQueue.Enqueue(sourceID)
	predecessor[sourceID] = -1
	visitedArticles[sourceID] = true

	for !bfsQueue.IsEmpty() {
		articleID := bfsQueue.Dequeue()

		adjacentArticles := adjacencyList[getRealID(articleID, redirectMap)]

		for _, adjacentArticleID := range adjacentArticles {
			realAdjacentArticleID := getRealID(adjacentArticleID, redirectMap)

			_, existVisitedArticle := visitedArticles[realAdjacentArticleID]
			if existVisitedArticle {
				continue
			}

			predecessor[adjacentArticleID] = articleID
			visitedArticles[realAdjacentArticleID] = true

			if realAdjacentArticleID == destinationID {
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
