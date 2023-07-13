package middlewares

import (
	"context"
	"github.com/haskaalo/wikisp/webapi/database"
	"github.com/haskaalo/wikisp/webapi/response"
	"log"
	"net/http"
)

const UserSessionContextKey = "user-sess"
const UserSessionQueryKey = "sess-token"
const MaxAPICall = 50

func GetSession(r *http.Request) *database.Session {
	sess, ok := r.Context().Value(UserSessionContextKey).(*database.Session)
	if !ok {
		return nil
	}
	return sess
}

// RequireSession return unauthorized in JSON if user is not verified by captcha
func RequireSession(next http.Handler) http.Handler {
	return http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		session := GetSession(r)
		if session == nil {
			response.Unauthorized(rw)
			return
		} else if session.APICallCount > MaxAPICall {
			_ = database.DeleteSessionBySelector(session.Selector)
			response.Unauthorized(rw)
			return
		}

		next.ServeHTTP(rw, r)
	})
}

// IncrementAPICallCount This function limit the amount of call from a session to MaxAPICall
func IncrementAPICallCount(next http.Handler) http.Handler {
	return http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		session := GetSession(r)
		if session == nil {
			next.ServeHTTP(rw, r)
			return
		}

		err := session.IncrementAPICallCount()
		if err != nil {
			response.InternalError(rw)
			log.Println(err)
			return
		}

		next.ServeHTTP(rw, r)
	})
}

// SetSession Set Session variable in request
func SetSession(next http.Handler) http.Handler {
	return http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		if !r.URL.Query().Has(UserSessionQueryKey) {
			next.ServeHTTP(rw, r)
			return
		}

		sessToken := r.URL.Query().Get(UserSessionQueryKey)
		sess, err := database.GetSessionByToken(sessToken)
		if err == database.ErrNotValidSessionToken {
			next.ServeHTTP(rw, r)
			return
		} else if err != nil {
			log.Println(err)
			next.ServeHTTP(rw, r)
			return
		}

		ctx := context.WithValue(r.Context(), UserSessionContextKey, sess)
		next.ServeHTTP(rw, r.WithContext(ctx))
	})
}
