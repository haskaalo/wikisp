package api

import (
	"encoding/json"
	"github.com/haskaalo/wikisp/webapi/database"
	"github.com/haskaalo/wikisp/webapi/response"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
)

type RecaptchaResponse struct {
	Success     bool   `json:"success"`
	HostName    string `json:"hostname"`
	ChallengeTS string `json:"challenge_ts"`
}

type getSessionTokenResponse struct {
	Success bool   `json:"success"`
	Token   string `json:"token,omitempty"`
}

// getSessionToken Validate if user is a robot through Google recaptcha
func getBotVerif(w http.ResponseWriter, r *http.Request) {
	if !r.URL.Query().Has("recaptchaResponse") {
		response.InvalidParameter(w, "recaptchaResponse")
		return
	}
	params := url.Values{}
	params.Add("secret", os.Getenv("RECAPTCHA_SECRET"))
	params.Add("response", r.URL.Query().Get("recaptchaResponse"))

	resp, err := http.Post("https://www.google.com/recaptcha/api/siteverify?"+params.Encode(),
		"application/x-www-form-urlencoded", strings.NewReader(""))
	if err != nil {
		response.InternalError(w)
		log.Println(err)
		return
	}

	respJSON := &RecaptchaResponse{}
	err = json.NewDecoder(resp.Body).Decode(respJSON)
	if err != nil {
		response.InternalError(w)
		log.Println(err)
		return
	}

	if respJSON.Success {
		selector, validator, err := database.InitiateSession()
		if err != nil {
			response.InternalError(w)
			log.Println(err)
			return
		}

		resp := getSessionTokenResponse{Success: true, Token: selector + "." + validator}
		response.Respond(w, &resp, http.StatusOK)
	} else {
		response.Respond(w, &getSessionTokenResponse{Success: false}, http.StatusOK)
	}
}
