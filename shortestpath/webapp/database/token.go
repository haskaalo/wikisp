package database

import "strings"

// Token user token
type Token struct {
	Selector  string
	Validator string
}

// ParseToken parse a token
func ParseToken(n string) (*Token, error) {
	token := new(Token)
	piece := strings.Split(n, ".")

	if len(piece) == 1 {
		return nil, ErrNotValidSessionToken
	}

	if piece[1] == "" {
		return nil, ErrNotValidSessionToken
	}

	token.Selector = piece[0]
	token.Validator = piece[1]

	return token, nil
}
