package routers

import (
	"database/sql"
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

type articleElement struct {
	OriginalTitle string `json:"original_title"`
	RedirectTo    string `json:"redirect_to_title"`
}

type getShortestPathResponse struct {
	Path []articleElement `json:"path"`
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
	if err == sql.ErrNoRows {
		response.InvalidParameter(w, "from")
		return
	} else if err != nil {
		response.InternalError(w)
		log.Println(err)
		return
	}

	toID, toComponentID, err := database.GetArticleIDsFromTitle(r.URL.Query().Get("to"))
	if err == sql.ErrNoRows {
		response.InvalidParameter(w, "to")
		return
	} else if err != nil {
		response.InternalError(w)
		log.Println(err)
		return
	}

	if fromComponentID != toComponentID {
		exist := articlepath.ExistPossiblePath(fromComponentID, toComponentID, componentAdjacencyList)
		if !exist {
			response.Respond(w, &getShortestPathResponse{Path: []articleElement{}}, http.StatusOK)
			return
		}
	}

	result := articlepath.ComputePathBFS(fromID, toID, articleAdjacencyList, redirectMap)
	var resultJSON []articleElement

	for _, articleID := range result {
		originalTitle, err := database.GetArticleTitleFromID(articleID)
		if err != nil {
			response.InternalError(w)
			return
		}

		redirectArticleID, exist := redirectMap[articleID]
		redirectTitle := ""

		if exist {
			redirectTitle, err = database.GetArticleTitleFromID(redirectArticleID)
			if err != nil {
				response.InternalError(w)
				return
			}
		}

		resultJSON = append(resultJSON, articleElement{OriginalTitle: originalTitle, RedirectTo: redirectTitle})
	}

	response.Respond(w, &getShortestPathResponse{Path: resultJSON}, http.StatusOK)
}
