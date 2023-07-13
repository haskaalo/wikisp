package utils

import (
	"crypto/rand"
	"math/big"
)

var letterRunes = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

// RandString return random string with specified length
func RandString(n int) string {
	b := make([]rune, n)

	for i := range b {
		randomLetterPosition, err := rand.Int(rand.Reader, big.NewInt(int64(len(letterRunes))))
		if err != nil {
			panic(err)
		}

		b[i] = letterRunes[randomLetterPosition.Int64()]
	}

	return string(b)
}
