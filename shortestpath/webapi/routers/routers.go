package routers

import (
	"github.com/go-chi/chi/v5"
	"github.com/haskaalo/wikisp/webapi/response"
	"log"
	"net/http"
	"os"
	"path/filepath"
)

// BootstrapRouters Create a router with every paths
func BootstrapRouters() *chi.Mux {
	log.Println("Deserializing wiki graph data")
	initSerializedData()
	log.Println("Done deserializing wiki graph data")
	response.InitTemplates()

	router := chi.NewRouter()
	assetsPath := os.Getenv("WIKISP_ASSETS_PATH")

	fs := http.FileServer(http.Dir(filepath.Join(assetsPath, "/static")))
	router.Handle("/static/*", http.StripPrefix("/static/", fs))

	router.Get("/", func(w http.ResponseWriter, r *http.Request) {
		response.Render(w, response.RenderData{
			Title: "WikiSP - Find paths between Wikipedia articles",
		})
	})
	router.Get("/search", getSearchTitle)
	router.Get("/find_path", getShortestPath)

	return router
}
