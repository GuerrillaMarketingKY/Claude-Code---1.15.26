package auth

import (
	"context"
	"crypto/rand"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"time"
)

const (
	AuthURL     = "https://app.clickup.com/api"
	TokenURL    = "https://api.clickup.com/api/v2/oauth/token"
	CallbackURL = "http://localhost:8089/callback"
)

type OAuthClient struct {
	ClientID     string
	ClientSecret string
	RedirectURI  string
	Storage      *TokenStorage
}

type OAuthResponse struct {
	AccessToken string `json:"access_token"`
	TokenType   string `json:"token_type"`
}

func NewOAuthClient(clientID, clientSecret string, storage *TokenStorage) *OAuthClient {
	return &OAuthClient{
		ClientID:     clientID,
		ClientSecret: clientSecret,
		RedirectURI:  CallbackURL,
		Storage:      storage,
	}
}

// StartAuthFlow initiates the OAuth flow and returns the authorization URL
func (c *OAuthClient) StartAuthFlow() (string, string, error) {
	// Generate secure random state
	state, err := generateState()
	if err != nil {
		return "", "", fmt.Errorf("failed to generate state: %w", err)
	}

	// Build authorization URL
	authURL := fmt.Sprintf("%s?client_id=%s&redirect_uri=%s",
		AuthURL,
		url.QueryEscape(c.ClientID),
		url.QueryEscape(c.RedirectURI),
	)

	return authURL, state, nil
}

// HandleCallback processes the OAuth callback and exchanges code for tokens
func (c *OAuthClient) HandleCallback(code string) error {
	// Exchange authorization code for access token
	tokenURL := fmt.Sprintf("%s?client_id=%s&client_secret=%s&code=%s",
		TokenURL,
		url.QueryEscape(c.ClientID),
		url.QueryEscape(c.ClientSecret),
		url.QueryEscape(code),
	)

	resp, err := http.Post(tokenURL, "application/json", nil)
	if err != nil {
		return fmt.Errorf("failed to exchange code for token: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("token exchange failed with status: %d", resp.StatusCode)
	}

	var tokenResp OAuthResponse
	if err := parseJSON(resp.Body, &tokenResp); err != nil {
		return fmt.Errorf("failed to parse token response: %w", err)
	}

	// Store the access token
	token := &Token{
		AccessToken: tokenResp.AccessToken,
		TokenType:   tokenResp.TokenType,
		ExpiresAt:   time.Now().Add(24 * time.Hour), // ClickUp tokens typically expire in 24h
	}

	if err := c.Storage.SaveToken(token); err != nil {
		return fmt.Errorf("failed to save token: %w", err)
	}

	return nil
}

// StartCallbackServer starts a local HTTP server to handle OAuth callback
func (c *OAuthClient) StartCallbackServer(ctx context.Context, expectedState string) (*Token, error) {
	tokenChan := make(chan *Token, 1)
	errChan := make(chan error, 1)

	server := &http.Server{
		Addr: ":8089",
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			code := r.URL.Query().Get("code")
			state := r.URL.Query().Get("state")

			// Verify state to prevent CSRF
			if state != expectedState {
				errChan <- fmt.Errorf("state mismatch: possible CSRF attack")
				http.Error(w, "Invalid state parameter", http.StatusBadRequest)
				return
			}

			if code == "" {
				errChan <- fmt.Errorf("no authorization code received")
				http.Error(w, "No authorization code", http.StatusBadRequest)
				return
			}

			// Exchange code for token
			if err := c.HandleCallback(code); err != nil {
				errChan <- err
				http.Error(w, "Failed to exchange code", http.StatusInternalServerError)
				return
			}

			// Get the saved token
			token, err := c.Storage.GetToken()
			if err != nil {
				errChan <- err
				http.Error(w, "Failed to retrieve token", http.StatusInternalServerError)
				return
			}

			tokenChan <- token

			// Send success response
			w.Header().Set("Content-Type", "text/html")
			fmt.Fprintf(w, `
				<html>
				<head><title>Authorization Successful</title></head>
				<body style="font-family: Arial; text-align: center; padding: 50px;">
					<h1 style="color: #7B68EE;">✅ Authorization Successful!</h1>
					<p>You can now close this window and return to the terminal.</p>
					<script>setTimeout(function(){ window.close(); }, 3000);</script>
				</body>
				</html>
			`)
		}),
	}

	// Start server in goroutine
	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			errChan <- fmt.Errorf("callback server error: %w", err)
		}
	}()

	// Wait for token or error with timeout
	select {
	case token := <-tokenChan:
		server.Shutdown(ctx)
		return token, nil
	case err := <-errChan:
		server.Shutdown(ctx)
		return nil, err
	case <-time.After(5 * time.Minute):
		server.Shutdown(ctx)
		return nil, fmt.Errorf("OAuth flow timeout after 5 minutes")
	case <-ctx.Done():
		server.Shutdown(ctx)
		return nil, ctx.Err()
	}
}

func generateState() (string, error) {
	b := make([]byte, 32)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return base64.URLEncoding.EncodeToString(b), nil
}

func parseJSON(r io.Reader, v interface{}) error {
	return json.NewDecoder(r).Decode(v)
}
