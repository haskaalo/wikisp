package routers

import "github.com/go-chi/chi/v5"

// BootstrapRouters Create a router with every paths
func BootstrapRouters() *chi.Mux {
	router := chi.NewRouter()
	router.Get("/search", GetSearchTitle)

	return router
}
