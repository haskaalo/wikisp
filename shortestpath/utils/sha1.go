package utils

import (
	"crypto/sha1"
	"crypto/sha256"
	"encoding/hex"
)

// SHA1 Hash data into SHA1 hex
func SHA1(n []byte) string {
	h := sha1.New()
	_, _ = h.Write(n)

	return hex.EncodeToString(h.Sum(nil))
}

// SHA256 Hash data into SHA256 hex
func SHA256(n []byte) string {
	h := sha256.New()
	_, _ = h.Write(n)

	return hex.EncodeToString(h.Sum(nil))
}
