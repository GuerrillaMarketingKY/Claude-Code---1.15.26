package clickup

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"

	"github.com/GuerrillaMarketingKY/clickup-claude-integration/internal/auth"
)

const (
	BaseURL = "https://api.clickup.com/api/v2"
)

type Client struct {
	accessToken string
	storage     *auth.TokenStorage
	httpClient  *http.Client
}

type Task struct {
	ID          string       `json:"id"`
	Name        string       `json:"name"`
	Description string       `json:"description"`
	Status      Status       `json:"status"`
	Priority    *Priority    `json:"priority"`
	Assignees   []Assignee   `json:"assignees"`
	Tags        []Tag        `json:"tags"`
	CustomFields []CustomField `json:"custom_fields"`
	DateCreated string       `json:"date_created"`
	DateUpdated string       `json:"date_updated"`
	URL         string       `json:"url"`
}

type Status struct {
	Status string `json:"status"`
	Color  string `json:"color"`
	Type   string `json:"type"`
}

type Priority struct {
	ID       string `json:"id"`
	Priority string `json:"priority"`
	Color    string `json:"color"`
}

type Assignee struct {
	ID       int    `json:"id"`
	Username string `json:"username"`
	Email    string `json:"email"`
}

type Tag struct {
	Name string `json:"name"`
}

type CustomField struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Value interface{} `json:"value"`
}

type TaskComment struct {
	CommentText string `json:"comment_text"`
}

// NewClient creates a client with an access token (for OAuth)
func NewClient(accessToken string) *Client {
	return &Client{
		accessToken: accessToken,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

// NewClientFromStorage creates a client using stored OAuth token
func NewClientFromStorage(storage *auth.TokenStorage) (*Client, error) {
	token, err := storage.GetToken()
	if err != nil {
		return nil, fmt.Errorf("failed to load token: %w", err)
	}

	return &Client{
		accessToken: token.AccessToken,
		storage:     storage,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}, nil
}

func (c *Client) GetTask(taskID string) (*Task, error) {
	url := fmt.Sprintf("%s/task/%s", BaseURL, taskID)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Authorization", c.accessToken)
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to execute request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("API returned status %d: %s", resp.StatusCode, string(body))
	}

	var task Task
	if err := json.NewDecoder(resp.Body).Decode(&task); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &task, nil
}

func (c *Client) UpdateTaskStatus(taskID, status string) error {
	url := fmt.Sprintf("%s/task/%s", BaseURL, taskID)

	payload := map[string]string{"status": status}
	jsonData, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("failed to marshal payload: %w", err)
	}

	req, err := http.NewRequest("PUT", url, strings.NewReader(string(jsonData)))
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Authorization", c.accessToken)
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("failed to execute request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("API returned status %d: %s", resp.StatusCode, string(body))
	}

	return nil
}

func (c *Client) AddComment(taskID string, comment string) error {
	url := fmt.Sprintf("%s/task/%s/comment", BaseURL, taskID)

	payload := TaskComment{CommentText: comment}
	jsonData, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("failed to marshal payload: %w", err)
	}

	req, err := http.NewRequest("POST", url, strings.NewReader(string(jsonData)))
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Authorization", c.accessToken)
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("failed to execute request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("API returned status %d: %s", resp.StatusCode, string(body))
	}

	return nil
}
