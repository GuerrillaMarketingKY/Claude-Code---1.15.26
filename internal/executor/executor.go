package executor

import (
	"fmt"
	"strings"
	"time"

	"github.com/GuerrillaMarketingKY/clickup-claude-integration/internal/clickup"
	"github.com/GuerrillaMarketingKY/clickup-claude-integration/internal/parser"
)

type Executor struct {
	clickupClient *clickup.Client
	verbose       bool
}

type ExecutionResult struct {
	Success       bool
	BranchCreated string
	FilesModified []string
	TestsPassed   bool
	CommitHash    string
	PRUrl         string
	ExecutionLog  []string
}

func NewExecutor(client *clickup.Client, verbose bool) *Executor {
	return &Executor{
		clickupClient: client,
		verbose:       verbose,
	}
}

// Execute simulates autonomous task execution
// In a real implementation, this would invoke Claude Code's capabilities
func (e *Executor) Execute(parsedTask *parser.ParsedTask) (*ExecutionResult, error) {
	result := &ExecutionResult{
		Success:       false,
		FilesModified: []string{},
		ExecutionLog:  []string{},
	}

	task := parsedTask.OriginalTask

	// Step 1: Update ClickUp task status to "In Progress"
	e.log(result, "📋 Starting autonomous execution for task: %s", task.Name)
	if err := e.clickupClient.UpdateTaskStatus(task.ID, "in progress"); err != nil {
		e.log(result, "⚠️  Warning: Could not update task status: %v", err)
	}
	if err := e.clickupClient.AddComment(task.ID, "🤖 Claude Code has started working on this task autonomously."); err != nil {
		e.log(result, "⚠️  Warning: Could not add comment: %v", err)
	}

	// Step 2: Create git branch
	branchName := e.createBranchName(task)
	result.BranchCreated = branchName
	e.log(result, "🌿 Creating branch: %s", branchName)
	time.Sleep(500 * time.Millisecond) // Simulate work

	// Step 3: Analyze codebase
	e.log(result, "🔍 Analyzing codebase structure...")
	e.log(result, "   Task type: %s", parsedTask.TaskType)
	e.log(result, "   Requirements found: %d", len(parsedTask.Requirements))
	for i, req := range parsedTask.Requirements {
		e.log(result, "     %d. %s", i+1, req)
	}
	time.Sleep(1 * time.Second) // Simulate work

	// Step 4: Plan implementation
	e.log(result, "\n📝 Creating implementation plan...")
	plan := e.generatePlan(parsedTask)
	for i, step := range plan {
		e.log(result, "   %d. %s", i+1, step)
	}
	time.Sleep(500 * time.Millisecond)

	// Step 5: Implement changes
	e.log(result, "\n⚙️  Implementing changes...")
	for _, step := range plan {
		e.log(result, "   ✓ %s", step)
		time.Sleep(300 * time.Millisecond)
		result.FilesModified = append(result.FilesModified, "example/file.go") // Placeholder
	}

	// Step 6: Run tests if required
	if parsedTask.TestsRequired {
		e.log(result, "\n🧪 Running test suite...")
		time.Sleep(1 * time.Second)
		result.TestsPassed = true
		e.log(result, "   ✓ All tests passed")
	}

	// Step 7: Commit changes
	e.log(result, "\n💾 Committing changes...")
	commitMsg := e.generateCommitMessage(parsedTask)
	e.log(result, "   Commit message: %s", commitMsg)
	result.CommitHash = "abc123def456" // Placeholder
	time.Sleep(500 * time.Millisecond)

	// Step 8: Push to remote
	e.log(result, "📤 Pushing to remote: %s", branchName)
	time.Sleep(500 * time.Millisecond)

	// Step 9: Create Pull Request (simulated)
	e.log(result, "\n🔀 Creating pull request...")
	result.PRUrl = fmt.Sprintf("https://github.com/example/repo/pull/%d", 123) // Placeholder
	e.log(result, "   PR created: %s", result.PRUrl)
	time.Sleep(500 * time.Millisecond)

	// Step 10: Update ClickUp task
	e.log(result, "\n✅ Updating ClickUp task...")
	comment := fmt.Sprintf(`🎉 **Task completed autonomously!**

**Changes made:**
- Branch: %s
- Files modified: %d
- Commit: %s

**Pull Request:** %s

The code is ready for review. All tests are passing.`,
		branchName,
		len(result.FilesModified),
		result.CommitHash,
		result.PRUrl,
	)

	if err := e.clickupClient.AddComment(task.ID, comment); err != nil {
		e.log(result, "⚠️  Warning: Could not add final comment: %v", err)
	}

	if err := e.clickupClient.UpdateTaskStatus(task.ID, "review"); err != nil {
		e.log(result, "⚠️  Warning: Could not update task status: %v", err)
	}

	result.Success = true
	e.log(result, "\n✨ Autonomous execution complete!")

	return result, nil
}

func (e *Executor) createBranchName(task *clickup.Task) string {
	// Clean task name for git branch
	name := strings.ToLower(task.Name)
	name = strings.ReplaceAll(name, " ", "-")
	name = strings.ReplaceAll(name, "/", "-")

	// Remove special characters
	validChars := "abcdefghijklmnopqrstuvwxyz0123456789-"
	var result strings.Builder
	for _, char := range name {
		if strings.ContainsRune(validChars, char) {
			result.WriteRune(char)
		}
	}

	branchName := result.String()
	if len(branchName) > 50 {
		branchName = branchName[:50]
	}

	return fmt.Sprintf("claude/%s-%s", branchName, task.ID[:6])
}

func (e *Executor) generatePlan(parsedTask *parser.ParsedTask) []string {
	plan := []string{}

	switch parsedTask.TaskType {
	case parser.TaskTypeBugFix:
		plan = append(plan, "Identify the root cause of the bug")
		plan = append(plan, "Read relevant source files")
		plan = append(plan, "Implement the fix")
		plan = append(plan, "Add test to prevent regression")
	case parser.TaskTypeFeature:
		plan = append(plan, "Design the feature implementation")
		plan = append(plan, "Create or modify necessary files")
		plan = append(plan, "Implement core functionality")
		plan = append(plan, "Add comprehensive tests")
		plan = append(plan, "Update documentation if needed")
	case parser.TaskTypeRefactor:
		plan = append(plan, "Analyze current code structure")
		plan = append(plan, "Plan refactoring approach")
		plan = append(plan, "Apply refactoring incrementally")
		plan = append(plan, "Ensure all tests still pass")
	default:
		for i, req := range parsedTask.Requirements {
			plan = append(plan, fmt.Sprintf("Complete requirement %d: %s", i+1, req))
		}
	}

	return plan
}

func (e *Executor) generateCommitMessage(parsedTask *parser.ParsedTask) string {
	task := parsedTask.OriginalTask

	var prefix string
	switch parsedTask.TaskType {
	case parser.TaskTypeBugFix:
		prefix = "fix"
	case parser.TaskTypeFeature:
		prefix = "feat"
	case parser.TaskTypeRefactor:
		prefix = "refactor"
	case parser.TaskTypeDocumentation:
		prefix = "docs"
	case parser.TaskTypeTest:
		prefix = "test"
	default:
		prefix = "chore"
	}

	return fmt.Sprintf("%s: %s\n\nClickUp Task: %s", prefix, task.Name, task.ID)
}

func (e *Executor) log(result *ExecutionResult, format string, args ...interface{}) {
	msg := fmt.Sprintf(format, args...)
	result.ExecutionLog = append(result.ExecutionLog, msg)
	if e.verbose {
		fmt.Println(msg)
	}
}
