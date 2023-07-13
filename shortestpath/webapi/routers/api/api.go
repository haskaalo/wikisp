package api

import (
	"github.com/go-chi/chi/v5"
	"github.com/haskaalo/wikisp/webapi/middlewares"
	"net/http"
)

func BootstrapAPIRouter(router chi.Router) http.Handler {
	router.Get("/search", getSearchTitle)
	router.Get("/random_article_titles", getRandomArticles)
	router.Get("/bot-verif", getBotVerif)

	g := router.Group(nil)
	g.Use(middlewares.SetSession)
	g.Use(middlewares.IncrementAPICallCount)
	g.Use(middlewares.RequireSession)
	g.Get("/find_path", getShortestPath)

	return router
}
