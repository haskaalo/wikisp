package routers

import (
	"github.com/haskaalo/wikisp/webapi/database"
	"github.com/haskaalo/wikisp/webapi/response"
	"log"
	"net/http"
)

type getSearchTitleResponse struct {
	Result []string `json:"result"`
}

func GetSearchTitle(w http.ResponseWriter, r *http.Request) {
	if !r.URL.Query().Has("q") {
		response.InvalidParameter(w, "q")
		return
	}

	searchQuery := r.URL.Query().Get("q")

	result, err := database.SearchArticle(searchQuery)
	if err != nil {
		log.Println(err)
		response.InternalError(w)
		return
	}

	responseJSON := getSearchTitleResponse{Result: result}
	response.Respond(w, &responseJSON, http.StatusOK)
}
