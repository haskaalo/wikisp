package response

import (
	"net/http"
)

type basicError struct {
	Status  int      `json:"status"`
	Message string   `json:"message"`
	Invalid []string `json:"invalid,omitempty"`
}

// InvalidParameter Respond a request with a 400 error specificing which parameters are invalid
func InvalidParameter(w http.ResponseWriter, invalid ...string) {
	Respond(w, &basicError{
		Status:  400,
		Message: "Invalid Parameter(s)",
		Invalid: invalid,
	}, http.StatusBadRequest)
}

// NotFound Respond with a Status 404 and a message "Resource not found"
func NotFound(w http.ResponseWriter) {
	Respond(w, &basicError{
		Status:  404,
		Message: "Resource not found",
	}, http.StatusNotFound)
}

// InternalError Respond with a status 500 and a message "Internal Server Error"
func InternalError(w http.ResponseWriter) {
	Respond(w, &basicError{
		Status:  500,
		Message: "Internal Server Error",
	}, http.StatusInternalServerError)
}

// Unauthorized Respond with a status 401 and a message "Unauthorized"
func Unauthorized(w http.ResponseWriter) {
	Respond(w, &basicError{
		Status:  401,
		Message: "Unauthorized",
	}, http.StatusUnauthorized)
}
