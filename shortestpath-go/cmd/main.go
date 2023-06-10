package main

import (
	"bytes"
	_ "embed"
	"encoding/gob"
	"fanor.dev/wikisp/shortestpath/serializer"
	"log"
	"time"
)

var (
	//go:embed wikisp_article_map.gob
	articleData    []byte
	articleAdjList serializer.ArticleAdjacencyList
)

func init() {
	log.Println("Decoding")
	dec := gob.NewDecoder(bytes.NewReader(articleData))

	err := dec.Decode(&articleAdjList)
	if err != nil {
		log.Fatal(err)
	}
	articleData = []byte{}
	log.Println("Done decoding")
}

func main() {
	time.Sleep(10 * time.Second)
	print("bebop")
}
