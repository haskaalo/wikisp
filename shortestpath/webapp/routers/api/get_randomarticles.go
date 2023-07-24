package api

import (
	"log"
	"net/http"

	"github.com/haskaalo/wikisp/webapp/database"
	"github.com/haskaalo/wikisp/webapp/response"
)

var randomArticleTitles []string

func getRandomArticles(w http.ResponseWriter, r *http.Request) {
	var err error
	if randomArticleTitles == nil {
		randomArticleTitles, err = database.GetRandomArticles(200)
		if err != nil {
			log.Println(err)
			response.InternalError(w)
			return
		}
	}

	response.Respond(w, randomArticleTitles, http.StatusOK)
}
