package routers

import "github.com/go-chi/chi/v5"

// BootstrapRouters Create a router with every paths
func BootstrapRouters() *chi.Mux {
	initSerializedData()
	router := chi.NewRouter()
	router.Get("/search", getSearchTitle)
	router.Get("/find_path", getShortestPath)
	return router
}
