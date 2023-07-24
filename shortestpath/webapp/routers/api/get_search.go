package api

import (
	"log"
	"net/http"

	"github.com/haskaalo/wikisp/webapp/database"
	"github.com/haskaalo/wikisp/webapp/response"
)

type getSearchTitleResponse struct {
	Result []string `json:"result"`
}

func getSearchTitle(w http.ResponseWriter, r *http.Request) {
	if !r.URL.Query().Has("q") {
		response.InvalidParameter(w, "q")
		return
	}

	searchQuery := r.URL.Query().Get("q")
	if searchQuery == "" {
		response.Respond(w, getSearchTitleResponse{Result: []string{}}, http.StatusOK)
		return
	}

	result, err := database.SearchArticle(searchQuery)
	if err != nil {
		log.Println(err)
		response.InternalError(w)
		return
	}

	responseJSON := getSearchTitleResponse{Result: result}
	response.Respond(w, &responseJSON, http.StatusOK)
}
