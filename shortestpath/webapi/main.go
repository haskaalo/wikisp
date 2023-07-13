package main

import (
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/haskaalo/wikisp/webapi/database"
	"github.com/haskaalo/wikisp/webapi/routers"
	"log"
	"net/http"
)

func main() {
	database.InitDatabase()
	database.InitRedis()
	r := chi.NewRouter()

	r.Use(middleware.Logger)
	r.Mount("/", routers.BootstrapRouters())

	r.Get("/test", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("testing"))
	})
	log.Println("Starting web server")
	_ = http.ListenAndServe(":3000", r)
}
