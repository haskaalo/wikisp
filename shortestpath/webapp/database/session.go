package database

import (
	"errors"
	"github.com/haskaalo/wikisp/utils"
	"strconv"
	"time"
)

type Session struct {
	Selector     string `redis:"selector"`
	Validator    string `redis:"validator"`
	CreatedAt    int    `redis:"created_at"`
	APICallCount int    `redis:"api_call_count"`
}

// ErrNotValidSessionToken Invalid token format
var ErrNotValidSessionToken = errors.New("Not a valid token")

const (
	// SessionExpireTime Session expire time for a token
	SessionExpireTime = time.Duration(1) * time.Hour

	// SessionPrefix Prefix used for a user session
	SessionPrefix = "session:"
)

// ResetTimeSession Reset time of a session based on config.ini Expire time
func (s Session) ResetTimeSession() error {
	hashSelector := utils.SHA1([]byte(s.Selector))

	err := r.Expire(SessionPrefix+hashSelector, SessionExpireTime).Err()
	if err != nil {
		return err
	}

	return nil
}

func (s Session) IncrementAPICallCount() error {
	hashS := utils.SHA1([]byte(s.Selector))
	s.APICallCount += 1
	err := r.HMSet(SessionPrefix+hashS, map[string]interface{}{
		"api_call_count": s.APICallCount + 1,
	}).Err()

	return err
}

// GetSessionBySelector Get Session model with a selector (string)
func GetSessionBySelector(selector string) (*Session, error) {
	sess := new(Session)
	hashSelector := utils.SHA1([]byte(selector))
	vals, err := r.HGetAll(SessionPrefix + hashSelector).Result()
	if len(vals) == 0 { // Only way to know if key doesn't exist
		return nil, ErrNotValidSessionToken
	}
	if err != nil {
		return nil, err
	}

	createdAt, err := strconv.Atoi(vals["createdat"])
	if err != nil {
		return nil, err
	}

	apiCallCount, err := strconv.Atoi(vals["api_call_count"])
	if err != nil {
		return nil, err
	}

	sess.Selector = selector
	sess.Validator = vals["validator"]
	sess.CreatedAt = createdAt
	sess.APICallCount = apiCallCount

	return sess, nil
}

func DeleteSessionBySelector(selector string) error {
	hashSelector := utils.SHA1([]byte(selector))

	return r.Del(SessionPrefix + hashSelector).Err()
}

// GetSessionByToken get Session with Token
func GetSessionByToken(token string) (*Session, error) {
	parsedToken, err := ParseToken(token)
	if err != nil {
		return nil, err
	}

	session, err := GetSessionBySelector(parsedToken.Selector)
	if err != nil {
		return nil, err
	}

	hashedValidator := utils.SHA1([]byte(parsedToken.Validator))
	if hashedValidator == session.Validator {
		return session, nil
	}

	return nil, ErrNotValidSessionToken
}

func InitiateSession() (selector string, validator string, err error) {
	// s for selector
	// v for validator
	// s for selector
	s := utils.RandString(12)
	v := utils.RandString(50)
	hashS := utils.SHA1([]byte(s))

	// Create new session
	// Validator acts as some sort of key
	err = r.HMSet(SessionPrefix+hashS, map[string]interface{}{
		"validator":      utils.SHA1([]byte(v)),
		"createdat":      time.Now().Unix(),
		"api_call_count": 0,
	}).Err()

	// Make sure the session expire being inactive for a while
	err = Session{
		Selector: s,
	}.ResetTimeSession()
	if err != nil {
		return "", "", err
	}

	return s, v, nil
}
