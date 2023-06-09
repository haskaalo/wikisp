package main

import (
	"fanor.dev/wikidg/shortestpath/articlepath"
	"fanor.dev/wikisp/shortestpath/serializer"
	"fanor.dev/wikisp/shortestpath/serializer/database"
	"github.com/aws/aws-lambda-go/lambda"
)

type RequestPathEvent struct {
	Source struct {
		ID          int `json:"id"`
		ComponentID int `json:"component_id"`
	} `json:"source"`

	Destination struct {
		ID          int `json:"id"`
		ComponentID int `json:"component_id"`
	} `json:"destination"`
}

var ArticleAdjacencyList serializer.ArticleAdjacencyList
var ComponentAdjacencyList serializer.ComponentAdjacencyList

func HandleRequest(event RequestPathEvent) ([]database.AdjacentArticle, error) {
	// Initialize component adj list if not initialized
	if len(ComponentAdjacencyList) == 0 {
		ComponentAdjacencyList = serializer.DeserializeComponentAdjacency()
	}

	// Check if we can quickly say that a path doesn't exist
	if (event.Source.ComponentID != event.Destination.ComponentID) && !articlepath.ExistPossiblePath(event.Source.ComponentID, event.Destination.ComponentID, ComponentAdjacencyList) {
		return []database.AdjacentArticle{}, nil
	}

	// Initialize Article adj list if not already initialized
	if len(ArticleAdjacencyList) == 0 {
		ArticleAdjacencyList = serializer.DeserializeArticleAdjacency()
	}

	return articlepath.ComputePathBFS(event.Source.ID, event.Destination.ID, ArticleAdjacencyList), nil
}

func main() {
	lambda.Start(HandleRequest)
}
