package response

import (
	"html/template"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

// RenderData all Variables used in templates
type RenderData struct {
	Title    string
	MetaData MetaData
}

// MetaData tags used in html
type MetaData struct {
}

var (
	templates *template.Template
)

// InitTemplates initialize templates
func InitTemplates() {
	assetsPath := os.Getenv("WIKISP_ASSETS_PATH")
	templates = template.Must(template.ParseGlob(filepath.Join(assetsPath, "/html/*")))

	// Reload templates every 3 seconds in case of change
	// TODO: Must change
	if os.Getenv("WIKISP_DEBUG") == "1" {
		go func() {
			for {
				templates = template.Must(template.ParseGlob(filepath.Join(assetsPath, "/html/*")))
				time.Sleep(3 * time.Second)
			}
		}()
	}
}

// Render render template html
func Render(w http.ResponseWriter, data RenderData) {
	_ = templates.ExecuteTemplate(w, "indexPage", data)
}
