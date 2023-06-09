package serializer

import (
	"encoding/gob"
	"fanor.dev/wikisp/shortestpath/serializer/database"
	"fmt"
	"log"
	"os"
	"path/filepath"
)

type ArticleAdjacencyList map[int][]database.AdjacentArticle

func DeserializeArticleAdjacency() ArticleAdjacencyList {
	file, err := os.Open(filepath.Join(os.Getenv("ADJACENCY_LIST_PATH"), "wikisp_article_map.data"))
	if err != nil {
		log.Fatalln(err)
	}

	dec := gob.NewDecoder(file)
	var articleAdjList ArticleAdjacencyList

	err = dec.Decode(&articleAdjList)
	if err != nil {
		log.Fatal(err)
	}

	return articleAdjList
}

func serializeArticleAdjacency() {
	adjacencyList := ArticleAdjacencyList{}

	database.InitDatabase()

	log.Println("SERIALIZATION: Fetching article ID list")

	articleList, err := database.GetArticleIDList()
	if err != nil {
		log.Fatal(err)
	}
	log.Println("SERIALIZATION: Done fetching article ID list")
	log.Println("SERIALIZATION: Starting building adjacency list\n")

	for _, articleID := range *articleList {
		_, exist := adjacencyList[articleID.ID]
		if exist {
			continue
		}

		performArticleBFS(articleID.ID, adjacencyList)
	}

	// Start writing to disk
	destination, err := os.Create(filepath.Join(os.Getenv("ADJACENCY_LIST_PATH"), "wikisp_article_map.data"))
	defer destination.Close()
	if err != nil {
		log.Fatal(err)
	}

	enc := gob.NewEncoder(destination)
	err = enc.Encode(adjacencyList)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("SERIALIZATION: Done serializing article adjacency list")
	database.CloseDatabase()
}

func performArticleBFS(articleID int, adjacencyList ArticleAdjacencyList) {
	bfsQueue := InitQueue()
	visitedArticles := map[int]bool{}

	bfsQueue.Enqueue(articleID)

	for !bfsQueue.IsEmpty() {
		articleID := bfsQueue.Dequeue()
		adjacentArticlesID, err := database.GetAdjacentArticles(articleID)
		if err != nil {
			log.Fatalln(err)
		}

		fmt.Print(fmt.Sprintf("\radjacency list size: %d queue size: %d", len(visitedArticles), bfsQueue.Size()))

		adjacencyList[articleID] = adjacentArticlesID

		for _, adjacentArticleID := range adjacentArticlesID {
			_, existVisitedArticle := visitedArticles[adjacentArticleID.FinalDestID]
			if existVisitedArticle {
				continue
			}

			_, existAdjacencyList := adjacencyList[adjacentArticleID.FinalDestID]
			if existAdjacencyList {
				continue
			}

			visitedArticles[adjacentArticleID.FinalDestID] = true
			bfsQueue.Enqueue(adjacentArticleID.FinalDestID)
		}
	}
}
