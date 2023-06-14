package routers

import (
	"fanor.dev/wikidg/shortestpath/articlepath"
	"github.com/haskaalo/wikisp/serializer"
	"github.com/haskaalo/wikisp/webapi/database"
	"github.com/haskaalo/wikisp/webapi/response"
	"log"
	"net/http"
)

var articleAdjacencyList serializer.ArticleAdjacencyList
var componentAdjacencyList serializer.ComponentAdjacencyList
var redirectMap serializer.RedirectMap

func initSerializedData() {
	articleAdjacencyList = serializer.DeserializeArticleAdjacency()
	componentAdjacencyList = serializer.DeserializeComponentAdjacency()
	redirectMap = serializer.DeserializeRedirectMap()
}

type getShortestPathResponse struct {
	Path []int `json:"path"`
}

func getShortestPath(w http.ResponseWriter, r *http.Request) {
	if !r.URL.Query().Has("from") {
		response.InvalidParameter(w, "from")
		return
	} else if !r.URL.Query().Has("to") {
		response.InvalidParameter(w, "to")
		return
	}

	fromID, fromComponentID, err := database.GetArticleIDsFromTitle(r.URL.Query().Get("from"))
	if err != nil {
		response.InternalError(w)
		log.Println(err)
		return
	}

	toID, toComponentID, err := database.GetArticleIDsFromTitle(r.URL.Query().Get("to"))
	if err != nil {
		response.InternalError(w)
		log.Println(err)
		return
	}

	if fromComponentID != toComponentID {
		exist := articlepath.ExistPossiblePath(fromComponentID, toComponentID, componentAdjacencyList)
		if !exist {
			response.Respond(w, &getShortestPathResponse{Path: []int{}}, http.StatusOK)
			return
		}
	}

	result := articlepath.ComputePathBFS(fromID, toID, articleAdjacencyList, redirectMap)
	response.Respond(w, &getShortestPathResponse{Path: result}, http.StatusOK)
}
