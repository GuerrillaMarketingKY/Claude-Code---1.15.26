package config

import (
	"fmt"
	"os"
)

type Config struct {
	ClickUpAPIToken string
	ClickUpTeamID   string
	GitHubRepo      string
}

// Load reads configuration from environment variables
func Load() (*Config, error) {
	apiToken := os.Getenv("CLICKUP_API_TOKEN")
	if apiToken == "" {
		return nil, fmt.Errorf("CLICKUP_API_TOKEN environment variable is required")
	}

	teamID := os.Getenv("CLICKUP_TEAM_ID")
	if teamID == "" {
		return nil, fmt.Errorf("CLICKUP_TEAM_ID environment variable is required")
	}

	githubRepo := os.Getenv("GITHUB_REPO")
	if githubRepo == "" {
		githubRepo = "default-repo" // Optional, can be inferred from git
	}

	return &Config{
		ClickUpAPIToken: apiToken,
		ClickUpTeamID:   teamID,
		GitHubRepo:      githubRepo,
	}, nil
}
