package main

import (
	"github.com/haskaalo/wikisp/serializer"
)

func main() {
	serializer.SerializeArticleAdjacency()
	serializer.SerializeComponentAdjacency()
	serializer.SerializeRedirectMap()
}
