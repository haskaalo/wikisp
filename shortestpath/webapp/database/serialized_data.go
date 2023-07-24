package database

import "github.com/haskaalo/wikisp/serializer"

var ArticleAdjacencyList serializer.ArticleAdjacencyList
var ComponentAdjacencyList serializer.ComponentAdjacencyList
var RedirectMap serializer.RedirectMap

func InitSerializedData() {
	ArticleAdjacencyList = serializer.DeserializeArticleAdjacency()
	ComponentAdjacencyList = serializer.DeserializeComponentAdjacency()
	RedirectMap = serializer.DeserializeRedirectMap()
}
