package config

import (
	"fmt"
	"os"
)

type Config struct {
	// OAuth Configuration
	OAuthClientID     string
	OAuthClientSecret string

	// Repository configuration
	GitHubRepo      string
}

// Load reads configuration from environment variables
func Load() (*Config, error) {
	clientID := os.Getenv("CLICKUP_CLIENT_ID")
	if clientID == "" {
		return nil, fmt.Errorf("CLICKUP_CLIENT_ID environment variable is required")
	}

	clientSecret := os.Getenv("CLICKUP_CLIENT_SECRET")
	if clientSecret == "" {
		return nil, fmt.Errorf("CLICKUP_CLIENT_SECRET environment variable is required")
	}

	githubRepo := os.Getenv("GITHUB_REPO")
	if githubRepo == "" {
		githubRepo = "default-repo" // Optional, can be inferred from git
	}

	return &Config{
		OAuthClientID:     clientID,
		OAuthClientSecret: clientSecret,
		GitHubRepo:        githubRepo,
	}, nil
}
