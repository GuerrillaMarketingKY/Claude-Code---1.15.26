package auth

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"time"
)

type Token struct {
	AccessToken  string    `json:"access_token"`
	RefreshToken string    `json:"refresh_token,omitempty"`
	TokenType    string    `json:"token_type"`
	ExpiresAt    time.Time `json:"expires_at"`
}

type TokenStorage struct {
	filePath   string
	encryption cipher.AEAD
}

func NewTokenStorage() (*TokenStorage, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return nil, fmt.Errorf("failed to get home directory: %w", err)
	}

	configDir := filepath.Join(homeDir, ".clickup-claude")
	if err := os.MkdirAll(configDir, 0700); err != nil {
		return nil, fmt.Errorf("failed to create config directory: %w", err)
	}

	filePath := filepath.Join(configDir, "tokens.enc")

	// Generate or load encryption key
	key, err := getOrCreateKey(configDir)
	if err != nil {
		return nil, fmt.Errorf("failed to get encryption key: %w", err)
	}

	// Create AES cipher
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, fmt.Errorf("failed to create cipher: %w", err)
	}

	aead, err := cipher.NewGCM(block)
	if err != nil {
		return nil, fmt.Errorf("failed to create GCM: %w", err)
	}

	return &TokenStorage{
		filePath:   filePath,
		encryption: aead,
	}, nil
}

func (s *TokenStorage) SaveToken(token *Token) error {
	// Serialize token to JSON
	data, err := json.Marshal(token)
	if err != nil {
		return fmt.Errorf("failed to marshal token: %w", err)
	}

	// Encrypt the data
	encrypted, err := s.encrypt(data)
	if err != nil {
		return fmt.Errorf("failed to encrypt token: %w", err)
	}

	// Write to file with secure permissions
	if err := os.WriteFile(s.filePath, encrypted, 0600); err != nil {
		return fmt.Errorf("failed to write token file: %w", err)
	}

	return nil
}

func (s *TokenStorage) GetToken() (*Token, error) {
	// Read encrypted file
	encrypted, err := os.ReadFile(s.filePath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, fmt.Errorf("no saved token found - please run 'clickup-claude auth' first")
		}
		return nil, fmt.Errorf("failed to read token file: %w", err)
	}

	// Decrypt the data
	data, err := s.decrypt(encrypted)
	if err != nil {
		return nil, fmt.Errorf("failed to decrypt token: %w", err)
	}

	// Deserialize token
	var token Token
	if err := json.Unmarshal(data, &token); err != nil {
		return nil, fmt.Errorf("failed to unmarshal token: %w", err)
	}

	// Check if token is expired
	if time.Now().After(token.ExpiresAt) {
		return nil, fmt.Errorf("token expired - please run 'clickup-claude auth' to re-authenticate")
	}

	return &token, nil
}

func (s *TokenStorage) HasToken() bool {
	_, err := os.Stat(s.filePath)
	return err == nil
}

func (s *TokenStorage) ClearToken() error {
	if err := os.Remove(s.filePath); err != nil && !os.IsNotExist(err) {
		return fmt.Errorf("failed to remove token file: %w", err)
	}
	return nil
}

func (s *TokenStorage) encrypt(plaintext []byte) ([]byte, error) {
	// Generate nonce
	nonce := make([]byte, s.encryption.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, err
	}

	// Encrypt and prepend nonce
	ciphertext := s.encryption.Seal(nonce, nonce, plaintext, nil)
	return ciphertext, nil
}

func (s *TokenStorage) decrypt(ciphertext []byte) ([]byte, error) {
	nonceSize := s.encryption.NonceSize()
	if len(ciphertext) < nonceSize {
		return nil, fmt.Errorf("ciphertext too short")
	}

	// Extract nonce and ciphertext
	nonce, ciphertext := ciphertext[:nonceSize], ciphertext[nonceSize:]

	// Decrypt
	plaintext, err := s.encryption.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return nil, err
	}

	return plaintext, nil
}

func getOrCreateKey(configDir string) ([]byte, error) {
	keyPath := filepath.Join(configDir, ".key")

	// Try to read existing key
	key, err := os.ReadFile(keyPath)
	if err == nil && len(key) == 32 {
		return key, nil
	}

	// Generate new key
	key = make([]byte, 32) // AES-256
	if _, err := rand.Read(key); err != nil {
		return nil, fmt.Errorf("failed to generate key: %w", err)
	}

	// Save key with secure permissions
	if err := os.WriteFile(keyPath, key, 0600); err != nil {
		return nil, fmt.Errorf("failed to save key: %w", err)
	}

	return key, nil
}
