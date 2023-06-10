package serializer

import (
	"encoding/gob"
	"fanor.dev/wikisp/shortestpath/serializer/database"
	"log"
	"os"
	"path/filepath"
)

type RedirectMap map[int]int

func SerializeRedirectMap() {
	redirectMap := RedirectMap{}

	database.InitDatabase()
	defer database.CloseDatabase()

	log.Println("SERIALIZATION: Fetching redirect list")
	redirectList, err := database.GetRedirectList()
	if err != nil {
		log.Fatalln(err)
	}
	log.Println("SERIALIZATION: Done fetching redirect list")

	for _, redirect := range *redirectList {
		redirectMap[redirect.From] = redirect.To
	}

	log.Println("SERIALIZATION: Starting writing to disk")
	// Start writing to disk
	destination, err := os.Create(filepath.Join(os.Getenv("ADJACENCY_LIST_PATH"), "wikisp_redirect_map.gob"))
	defer destination.Close()
	if err != nil {
		log.Fatal(err)
	}

	enc := gob.NewEncoder(destination)
	err = enc.Encode(&redirectMap)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("SERIALIZATION: Done writing to disk")
}

func DeserializeRedirectMap() RedirectMap {
	file, err := os.Open(filepath.Join(os.Getenv("ADJACENCY_LIST_PATH"), "wikisp_redirect_map.gob"))
	if err != nil {
		log.Fatalln(err)
	}

	dec := gob.NewDecoder(file)
	var redirectMap RedirectMap

	err = dec.Decode(&redirectMap)
	if err != nil {
		log.Fatal(err)
	}

	return redirectMap
}
