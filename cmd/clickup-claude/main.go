package main

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"runtime"

	"github.com/GuerrillaMarketingKY/clickup-claude-integration/internal/auth"
	"github.com/GuerrillaMarketingKY/clickup-claude-integration/internal/clickup"
	"github.com/GuerrillaMarketingKY/clickup-claude-integration/internal/executor"
	"github.com/GuerrillaMarketingKY/clickup-claude-integration/internal/parser"
	"github.com/GuerrillaMarketingKY/clickup-claude-integration/pkg/config"
)

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	command := os.Args[1]

	switch command {
	case "auth":
		runAuth()
	case "logout":
		runLogout()
	case "execute":
		if len(os.Args) < 3 {
			fmt.Println("Error: Task ID required")
			fmt.Println("Usage: clickup-claude execute <task-id>")
			os.Exit(1)
		}
		taskID := os.Args[2]
		executeTaskOAuth(taskID)
	case "status":
		if len(os.Args) < 3 {
			fmt.Println("Error: Task ID required")
			fmt.Println("Usage: clickup-claude status <task-id>")
			os.Exit(1)
		}
		taskID := os.Args[2]
		showTaskStatusOAuth(taskID)
	case "help":
		printUsage()
	default:
		fmt.Printf("Unknown command: %s\n\n", command)
		printUsage()
		os.Exit(1)
	}
}


func displayTaskInfo(task *clickup.Task) {
	fmt.Println("┌─────────────────────────────────────────────────┐")
	fmt.Printf("│ Task: %-41s │\n", truncate(task.Name, 41))
	fmt.Println("├─────────────────────────────────────────────────┤")
	fmt.Printf("│ ID:       %-39s │\n", task.ID)
	fmt.Printf("│ Status:   %-39s │\n", task.Status.Status)
	if task.Priority != nil {
		fmt.Printf("│ Priority: %-39s │\n", task.Priority.Priority)
	}
	fmt.Printf("│ URL:      %-39s │\n", truncate(task.URL, 39))
	fmt.Println("└─────────────────────────────────────────────────┘")

	if task.Description != "" {
		fmt.Println("\n📝 Description:")
		fmt.Println("─────────────────────────────────────────────────")
		fmt.Println(task.Description)
		fmt.Println("─────────────────────────────────────────────────")
	}
}

func printUsage() {
	fmt.Println("ClickUp Claude - Autonomous Task Execution")
	fmt.Println()
	fmt.Println("Usage:")
	fmt.Println("  clickup-claude auth                Authenticate with ClickUp OAuth")
	fmt.Println("  clickup-claude logout              Clear stored authentication")
	fmt.Println("  clickup-claude execute <task-id>   Execute a ClickUp task autonomously")
	fmt.Println("  clickup-claude status <task-id>    Show task information")
	fmt.Println("  clickup-claude help                Show this help message")
	fmt.Println()
	fmt.Println("Environment Variables:")
	fmt.Println("  CLICKUP_CLIENT_ID       Your ClickUp OAuth Client ID (required)")
	fmt.Println("  CLICKUP_CLIENT_SECRET   Your ClickUp OAuth Client Secret (required)")
	fmt.Println("  GITHUB_REPO             GitHub repository name (optional)")
	fmt.Println()
	fmt.Println("Getting Started:")
	fmt.Println("  1. Create a ClickUp OAuth app: https://app.clickup.com/settings/apps")
	fmt.Println("  2. Set environment variables with your OAuth credentials")
	fmt.Println("  3. Run 'clickup-claude auth' to authenticate")
	fmt.Println("  4. Run 'clickup-claude execute <task-id>' to execute tasks")
	fmt.Println()
	fmt.Println("Example:")
	fmt.Println("  export CLICKUP_CLIENT_ID='your_client_id'")
	fmt.Println("  export CLICKUP_CLIENT_SECRET='your_client_secret'")
	fmt.Println("  clickup-claude auth")
	fmt.Println("  clickup-claude execute abc123")
}

func getStatusEmoji(success bool) string {
	if success {
		return "✅ Success"
	}
	return "❌ Failed"
}

func truncate(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen-3] + "..."
}

func runAuth() {
	fmt.Println("🔐 ClickUp OAuth Authentication")
	fmt.Println("================================\n")

	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		fmt.Printf("❌ Configuration error: %v\n", err)
		fmt.Println("\nPlease set the following environment variables:")
		fmt.Println("  - CLICKUP_CLIENT_ID")
		fmt.Println("  - CLICKUP_CLIENT_SECRET")
		os.Exit(1)
	}

	// Create token storage
	storage, err := auth.NewTokenStorage()
	if err != nil {
		fmt.Printf("❌ Failed to create token storage: %v\n", err)
		os.Exit(1)
	}

	// Create OAuth client
	oauthClient := auth.NewOAuthClient(cfg.OAuthClientID, cfg.OAuthClientSecret, storage)

	// Start OAuth flow
	authURL, state, err := oauthClient.StartAuthFlow()
	if err != nil {
		fmt.Printf("❌ Failed to start OAuth flow: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("📋 Step 1: Opening browser for authorization...")
	fmt.Printf("   URL: %s\n\n", authURL)

	// Open browser
	if err := openBrowser(authURL); err != nil {
		fmt.Printf("⚠️  Could not open browser automatically: %v\n", err)
		fmt.Printf("\nPlease open this URL manually:\n%s\n\n", authURL)
	}

	fmt.Println("📋 Step 2: Waiting for authorization...")
	fmt.Println("   (Please authorize the application in your browser)")

	// Start callback server and wait for token
	ctx := context.Background()
	token, err := oauthClient.StartCallbackServer(ctx, state)
	if err != nil {
		fmt.Printf("\n❌ Authorization failed: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("\n✅ Authentication successful!")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Printf("Access Token: %s...%s\n", token.AccessToken[:8], token.AccessToken[len(token.AccessToken)-8:])
	fmt.Printf("Expires At:   %s\n", token.ExpiresAt.Format("2006-01-02 15:04:05"))
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("\n🎉 You can now use 'clickup-claude execute <task-id>' to run tasks!")
}

func runLogout() {
	storage, err := auth.NewTokenStorage()
	if err != nil {
		fmt.Printf("❌ Failed to access token storage: %v\n", err)
		os.Exit(1)
	}

	if err := storage.ClearToken(); err != nil {
		fmt.Printf("❌ Failed to clear token: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("✅ Logged out successfully!")
	fmt.Println("   Run 'clickup-claude auth' to authenticate again.")
}

func executeTaskOAuth(taskID string) {
	fmt.Println("🚀 ClickUp Claude - Autonomous Task Execution")
	fmt.Println("============================================\n")

	// Create token storage
	storage, err := auth.NewTokenStorage()
	if err != nil {
		fmt.Printf("❌ Failed to create token storage: %v\n", err)
		os.Exit(1)
	}

	// Create ClickUp client from stored token
	fmt.Printf("🔑 Loading authentication token...\n")
	client, err := clickup.NewClientFromStorage(storage)
	if err != nil {
		fmt.Printf("❌ %v\n", err)
		fmt.Println("\n💡 Tip: Run 'clickup-claude auth' to authenticate first.")
		os.Exit(1)
	}
	fmt.Println("✓ Authentication loaded\n")

	// Fetch task
	fmt.Printf("📥 Fetching task %s from ClickUp...\n", taskID)
	task, err := client.GetTask(taskID)
	if err != nil {
		fmt.Printf("❌ Failed to fetch task: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("✓ Task fetched: %s\n\n", task.Name)

	// Display task information
	displayTaskInfo(task)

	// Parse task
	fmt.Println("\n🔍 Parsing task requirements...")
	parsedTask := parser.Parse(task)

	fmt.Printf("✓ Task type identified: %s\n", parsedTask.TaskType)
	fmt.Printf("✓ Requirements extracted: %d\n", len(parsedTask.Requirements))
	fmt.Printf("✓ Tests required: %v\n", parsedTask.TestsRequired)

	// Execute task autonomously
	fmt.Println("\n🤖 Beginning autonomous execution...\n")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	exec := executor.NewExecutor(client, true)
	result, err := exec.Execute(parsedTask)
	if err != nil {
		fmt.Printf("\n❌ Execution failed: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	// Display results
	fmt.Println("\n📊 Execution Summary")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Printf("Status:           %s\n", getStatusEmoji(result.Success))
	fmt.Printf("Branch Created:   %s\n", result.BranchCreated)
	fmt.Printf("Files Modified:   %d\n", len(result.FilesModified))
	fmt.Printf("Tests Passed:     %v\n", result.TestsPassed)
	fmt.Printf("Commit Hash:      %s\n", result.CommitHash)
	fmt.Printf("Pull Request:     %s\n", result.PRUrl)
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	if result.Success {
		fmt.Println("\n✨ Task completed successfully!")
		fmt.Println("   The ClickUp task has been updated with the results.")
	}
}

func showTaskStatusOAuth(taskID string) {
	// Create token storage
	storage, err := auth.NewTokenStorage()
	if err != nil {
		fmt.Printf("❌ Failed to create token storage: %v\n", err)
		os.Exit(1)
	}

	// Create client from stored token
	client, err := clickup.NewClientFromStorage(storage)
	if err != nil {
		fmt.Printf("❌ %v\n", err)
		fmt.Println("\n💡 Tip: Run 'clickup-claude auth' to authenticate first.")
		os.Exit(1)
	}

	fmt.Printf("📥 Fetching task %s...\n\n", taskID)
	task, err := client.GetTask(taskID)
	if err != nil {
		fmt.Printf("❌ Failed to fetch task: %v\n", err)
		os.Exit(1)
	}

	displayTaskInfo(task)
}

func openBrowser(url string) error {
	var cmd string
	var args []string

	switch runtime.GOOS {
	case "windows":
		cmd = "cmd"
		args = []string{"/c", "start", url}
	case "darwin":
		cmd = "open"
		args = []string{url}
	default: // linux, freebsd, etc.
		cmd = "xdg-open"
		args = []string{url}
	}

	return exec.Command(cmd, args...).Start()
}
