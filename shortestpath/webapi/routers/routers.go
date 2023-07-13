package routers

import (
	"github.com/go-chi/chi/v5"
	"github.com/haskaalo/wikisp/webapi/database"
	"github.com/haskaalo/wikisp/webapi/response"
	"github.com/haskaalo/wikisp/webapi/routers/api"
	"log"
	"net/http"
	"os"
)

// BootstrapRouters Create a router with every paths
func BootstrapRouters() *chi.Mux {
	log.Println("Deserializing wiki graph data")
	database.InitSerializedData()
	log.Println("Done deserializing wiki graph data")
	response.InitTemplates()

	router := chi.NewRouter()

	router.Get("/", func(w http.ResponseWriter, r *http.Request) {
		response.Render(w, response.RenderData{
			Title: "WikiSP - Find paths between Wikipedia articles",
		})
	})
	router.Route("/api", func(r chi.Router) {
		api.BootstrapAPIRouter(r)
	})
	assetsPath := os.Getenv("WIKISP_ASSETS_PATH")
	fs := http.FileServer(http.Dir(assetsPath))
	router.Handle("/*", http.StripPrefix("/", fs))

	return router
}
