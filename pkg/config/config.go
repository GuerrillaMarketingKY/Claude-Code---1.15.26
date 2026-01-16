package config

import (
	"fmt"
	"os"
)

type Config struct {
	// Direct Access Token (preferred)
	AccessToken string

	// OAuth Configuration (optional)
	OAuthClientID     string
	OAuthClientSecret string

	// Repository configuration
	GitHubRepo string
}

// Load reads configuration from environment variables
func Load() (*Config, error) {
	// Check for direct access token first (simpler method)
	accessToken := os.Getenv("CLICKUP_ACCESS_TOKEN")

	githubRepo := os.Getenv("GITHUB_REPO")
	if githubRepo == "" {
		githubRepo = "default-repo" // Optional, can be inferred from git
	}

	cfg := &Config{
		AccessToken:       accessToken,
		OAuthClientID:     os.Getenv("CLICKUP_CLIENT_ID"),
		OAuthClientSecret: os.Getenv("CLICKUP_CLIENT_SECRET"),
		GitHubRepo:        githubRepo,
	}

	// Validate that we have either direct token or OAuth credentials
	if cfg.AccessToken == "" && (cfg.OAuthClientID == "" || cfg.OAuthClientSecret == "") {
		return nil, fmt.Errorf("either CLICKUP_ACCESS_TOKEN or both CLICKUP_CLIENT_ID and CLICKUP_CLIENT_SECRET are required")
	}

	return cfg, nil
}
