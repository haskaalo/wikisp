package articlepath

import (
	"fanor.dev/wikisp/shortestpath/serializer"
	"fanor.dev/wikisp/shortestpath/serializer/database"
)

type PredecessorMap map[int]database.AdjacentArticle

func generatePredecessorPath(predecessor PredecessorMap, dest database.AdjacentArticle) []database.AdjacentArticle {
	var result []database.AdjacentArticle

	for dest.FinalDestID != -1 {
		// Add at index 0
		newResult := make([]database.AdjacentArticle, len(result)+1)
		newResult[0] = dest
		copy(newResult[1:], result)

		result = newResult

		// next iteration
		dest = predecessor[dest.FinalDestID]
	}

	return result
}

func ComputePathBFS(sourceID int, destinationID int, adjacencyList serializer.ArticleAdjacencyList) []database.AdjacentArticle {
	bfsQueue := InitArticleQueue()
	predecessor := PredecessorMap{}

	bfsQueue.Enqueue(database.AdjacentArticle{FinalDestID: sourceID,
		OriginalDestID: sourceID})
	predecessor[sourceID] = database.AdjacentArticle{FinalDestID: -1}

	for !bfsQueue.IsEmpty() {
		articleID := bfsQueue.Dequeue()

		adjacentArticlesID := adjacencyList[articleID.FinalDestID]

		for _, adjacentArticleID := range adjacentArticlesID {
			_, existVisitedArticle := predecessor[adjacentArticleID.FinalDestID]
			if existVisitedArticle {
				continue
			}

			predecessor[adjacentArticleID.FinalDestID] = articleID
			if adjacentArticleID.FinalDestID == destinationID {
				return generatePredecessorPath(predecessor, adjacentArticleID)
			}

			bfsQueue.Enqueue(adjacentArticleID)
		}
	}

	return []database.AdjacentArticle{}
}

func ExistPossiblePath(sourceID int, destinationID int, adjacencyList serializer.ComponentAdjacencyList) bool {
	bfsQueue := serializer.InitQueue()
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
