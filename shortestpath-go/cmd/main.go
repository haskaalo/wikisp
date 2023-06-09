package main

import (
	"fanor.dev/wikisp/shortestpath/serializer"
	"time"
)

func main() {
	x := serializer.DeserializeArticleAdjacency()
	print("done!")
	time.Sleep(10 * time.Second)
	print(x[100])
}
