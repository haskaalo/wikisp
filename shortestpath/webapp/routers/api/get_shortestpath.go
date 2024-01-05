package api

import (
	"database/sql"
	"log"
	"net/http"
	"strings"

	"github.com/haskaalo/wikisp/articlepath"
	"github.com/haskaalo/wikisp/webapp/database"
	"github.com/haskaalo/wikisp/webapp/response"
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
	capitalizedFromTitle := strings.ToUpper(fromTitle[:1]) + fromTitle[1:]
	fromID, fromComponentID, err := database.GetArticleIDsFromTitle(capitalizedFromTitle)
	if err == sql.ErrNoRows {
		response.InvalidParameter(w, fromTitle)
		return
	} else if err != nil {
		response.InternalError(w)
		log.Println(err)
		return
	}

	toTitle := r.URL.Query().Get("to")
	capitalizedToTitle := strings.ToUpper((toTitle[:1])) + toTitle[1:]
	toID, toComponentID, err := database.GetArticleIDsFromTitle(capitalizedToTitle)
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
	resultJSON := []articleElement{}

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
