package serializer

import (
	"encoding/gob"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/haskaalo/wikisp/utils"

	"github.com/haskaalo/wikisp/serializer/database"
)

type ComponentAdjacencyList map[int][]int

func DeserializeComponentAdjacency() ComponentAdjacencyList {
	file, err := os.Open(filepath.Join(os.Getenv("ADJACENCY_LIST_PATH"), "wikisp_component_map.gob"))
	if err != nil {
		log.Fatalln(err)
	}

	dec := gob.NewDecoder(file)
	var articleAdjList ComponentAdjacencyList

	err = dec.Decode(&articleAdjList)
	if err != nil {
		log.Fatal(err)
	}

	return articleAdjList
}

func SerializeComponentAdjacency() {
	adjacencyList := ComponentAdjacencyList{}

	database.InitDatabase()
	defer database.CloseDatabase()

	log.Println("SERIALIZATION: Fetching component ID list")
	componentList, err := database.GetArticleComponentIDList()
	if err != nil {
		log.Fatalln(err)
	}
	log.Println("SERIALIZATION: Done fetching component ID list")
	log.Println("SERIALIZATION: Starting building adjacency list\n")

	for _, component := range *componentList {
		_, exist := adjacencyList[component.ID]
		if exist {
			continue
		}

		performComponentBFS(component.ID, adjacencyList)
	}

	// Start writing to disk
	log.Println("SERIALIZATION: Starting writing to disk")
	destination, err := os.Create(filepath.Join(os.Getenv("ADJACENCY_LIST_PATH"), "wikisp_component_map.gob"))
	defer destination.Close()
	if err != nil {
		log.Fatal(err)
	}
	enc := gob.NewEncoder(destination)
	err = enc.Encode(&adjacencyList)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("SERIALIZATION: Done serializing component adjacency list")
}

func performComponentBFS(componentID int, adjacencyList ComponentAdjacencyList) {
	bfsQueue := utils.InitQueue()
	visitedComponents := map[int]bool{}

	bfsQueue.Enqueue(componentID)

	for !bfsQueue.IsEmpty() {
		componentID := bfsQueue.Dequeue()
		adjacentComponents, err := database.GetAdjacentComponents(componentID)
		if err != nil {
			log.Fatalln(err)
		}

		fmt.Print(fmt.Sprintf("\r adjacency list size: %d queue size: %d", len(visitedComponents), bfsQueue.Size()))

		adjacencyList[componentID] = []int{}

		for _, adjacentComponent := range adjacentComponents {
			adjacencyList[componentID] = append(adjacencyList[componentID], adjacentComponent.ID)

			_, existVisitedArticle := visitedComponents[adjacentComponent.ID]
			if existVisitedArticle {
				continue
			}

			_, existAdjacencyList := adjacencyList[adjacentComponent.ID]
			if existAdjacencyList {
				continue
			}

			visitedComponents[adjacentComponent.ID] = true
			bfsQueue.Enqueue(adjacentComponent.ID)
		}
	}
}
