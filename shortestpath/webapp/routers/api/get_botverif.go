package api

import (
	"encoding/json"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"

	"github.com/haskaalo/wikisp/webapp/database"
	"github.com/haskaalo/wikisp/webapp/response"
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
	if !r.URL.Query().Has("captchaResponse") {
		response.InvalidParameter(w, "captchaResponse")
		return
	}
	params := url.Values{}
	params.Add("secret", os.Getenv("CAPTCHA_SECRET"))
	params.Add("response", r.URL.Query().Get("captchaResponse"))

	resp, err := http.Post("https://challenges.cloudflare.com/turnstile/v0/siteverify",
		"application/x-www-form-urlencoded", strings.NewReader(params.Encode()))
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
