package routers

import (
	"database/sql"
	"fanor.dev/wikidg/shortestpath/articlepath"
	"github.com/haskaalo/wikisp/webapi/database"
	"github.com/haskaalo/wikisp/webapi/response"
	"log"
	"net/http"
)

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

	fromTitle := r.URL.Query().Get("from")
	fromID, fromComponentID, err := database.GetArticleIDsFromTitle(fromTitle)
	if err == sql.ErrNoRows {
		response.InvalidParameter(w, fromTitle)
		return
	} else if err != nil {
		response.InternalError(w)
		log.Println(err)
		return
	}

	toTitle := r.URL.Query().Get("to")
	toID, toComponentID, err := database.GetArticleIDsFromTitle(toTitle)
	if err == sql.ErrNoRows {
		response.InvalidParameter(w, toTitle)
		return
	} else if err != nil {
		response.InternalError(w)
		log.Println(err)
		return
	}

	if fromComponentID != toComponentID {
		exist := articlepath.ExistPossiblePath(fromComponentID, toComponentID, database.ComponentAdjacencyList)
		if !exist {
			response.Respond(w, &getShortestPathResponse{Path: []articleElement{}}, http.StatusOK)
			return
		}
	}

	result := articlepath.ComputePathBFS(fromID, toID, database.ArticleAdjacencyList, database.RedirectMap)
	var resultJSON []articleElement

	for _, articleID := range result {
		originalTitle, err := database.GetArticleTitleFromID(articleID)
		if err != nil {
			response.InternalError(w)
			return
		}

		redirectArticleID, exist := database.RedirectMap[articleID]
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
