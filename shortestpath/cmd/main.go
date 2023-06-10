package main

import (
	"fanor.dev/wikisp/shortestpath/serializer"
)

func main() {
	serializer.SerializeArticleAdjacency()
	serializer.SerializeComponentAdjacency()
	serializer.SerializeRedirectMap()
}
