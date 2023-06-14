package response

import (
	"encoding/json"
	"net/http"
)

// M Act as an alias for map[string]interface{}
type M map[string]interface{}

// Respond respond a request with JSON
func Respond(w http.ResponseWriter, in interface{}, status int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(in)
}
