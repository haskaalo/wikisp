package api

import (
	"github.com/haskaalo/wikisp/webapi/database"
	"github.com/haskaalo/wikisp/webapi/response"
	"log"
	"net/http"
)

var randomArticleTitles []string

func getRandomArticles(w http.ResponseWriter, r *http.Request) {
	var err error
	if randomArticleTitles == nil {
		// TODO: Fix this
		randomArticleTitles, err = database.GetRandomArticles(200)
		if err != nil {
			log.Println(err)
			response.InternalError(w)
			return
		}
	}

	response.Respond(w, randomArticleTitles, http.StatusOK)
}
