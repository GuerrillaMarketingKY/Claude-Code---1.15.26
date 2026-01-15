package main

import (
	"fmt"
	"os"

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
	case "execute":
		if len(os.Args) < 3 {
			fmt.Println("Error: Task ID required")
			fmt.Println("Usage: clickup-claude execute <task-id>")
			os.Exit(1)
		}
		taskID := os.Args[2]
		executeTask(taskID)
	case "status":
		if len(os.Args) < 3 {
			fmt.Println("Error: Task ID required")
			fmt.Println("Usage: clickup-claude status <task-id>")
			os.Exit(1)
		}
		taskID := os.Args[2]
		showTaskStatus(taskID)
	case "help":
		printUsage()
	default:
		fmt.Printf("Unknown command: %s\n\n", command)
		printUsage()
		os.Exit(1)
	}
}

func executeTask(taskID string) {
	fmt.Println("🚀 ClickUp Claude - Autonomous Task Execution")
	fmt.Println("============================================\n")

	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		fmt.Printf("❌ Configuration error: %v\n", err)
		fmt.Println("\nPlease set the following environment variables:")
		fmt.Println("  - CLICKUP_API_TOKEN")
		fmt.Println("  - CLICKUP_TEAM_ID")
		os.Exit(1)
	}

	// Create ClickUp client
	client := clickup.NewClient(cfg.ClickUpAPIToken)

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

func showTaskStatus(taskID string) {
	cfg, err := config.Load()
	if err != nil {
		fmt.Printf("❌ Configuration error: %v\n", err)
		os.Exit(1)
	}

	client := clickup.NewClient(cfg.ClickUpAPIToken)

	fmt.Printf("📥 Fetching task %s...\n\n", taskID)
	task, err := client.GetTask(taskID)
	if err != nil {
		fmt.Printf("❌ Failed to fetch task: %v\n", err)
		os.Exit(1)
	}

	displayTaskInfo(task)
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
	fmt.Println("  clickup-claude execute <task-id>   Execute a ClickUp task autonomously")
	fmt.Println("  clickup-claude status <task-id>    Show task information")
	fmt.Println("  clickup-claude help                Show this help message")
	fmt.Println()
	fmt.Println("Environment Variables:")
	fmt.Println("  CLICKUP_API_TOKEN    Your ClickUp API token (required)")
	fmt.Println("  CLICKUP_TEAM_ID      Your ClickUp team/workspace ID (required)")
	fmt.Println("  GITHUB_REPO          GitHub repository name (optional)")
	fmt.Println()
	fmt.Println("Example:")
	fmt.Println("  export CLICKUP_API_TOKEN='pk_your_token_here'")
	fmt.Println("  export CLICKUP_TEAM_ID='123456'")
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
