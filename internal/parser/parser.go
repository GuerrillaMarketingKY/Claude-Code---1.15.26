package parser

import (
	"regexp"
	"strings"

	"github.com/GuerrillaMarketingKY/clickup-claude-integration/internal/clickup"
)

type ParsedTask struct {
	OriginalTask    *clickup.Task
	TaskType        TaskType
	Requirements    []string
	AcceptanceCriteria []string
	FilesToModify   []string
	TestsRequired   bool
}

type TaskType string

const (
	TaskTypeBugFix      TaskType = "bug_fix"
	TaskTypeFeature     TaskType = "feature"
	TaskTypeRefactor    TaskType = "refactor"
	TaskTypeDocumentation TaskType = "documentation"
	TaskTypeTest        TaskType = "test"
	TaskTypeUnknown     TaskType = "unknown"
)

// Parse extracts structured information from a ClickUp task
func Parse(task *clickup.Task) *ParsedTask {
	parsed := &ParsedTask{
		OriginalTask:    task,
		Requirements:    []string{},
		AcceptanceCriteria: []string{},
		FilesToModify:   []string{},
		TestsRequired:   false,
	}

	// Determine task type from name and tags
	parsed.TaskType = determineTaskType(task)

	// Extract requirements from description
	parsed.Requirements = extractRequirements(task.Description)

	// Extract acceptance criteria
	parsed.AcceptanceCriteria = extractAcceptanceCriteria(task.Description)

	// Extract file paths mentioned in description
	parsed.FilesToModify = extractFilePaths(task.Description)

	// Check if tests are required
	parsed.TestsRequired = checkTestsRequired(task.Description, task.Tags)

	return parsed
}

func determineTaskType(task *clickup.Task) TaskType {
	nameLower := strings.ToLower(task.Name)

	// Check tags first
	for _, tag := range task.Tags {
		tagLower := strings.ToLower(tag.Name)
		switch {
		case strings.Contains(tagLower, "bug"):
			return TaskTypeBugFix
		case strings.Contains(tagLower, "feature"):
			return TaskTypeFeature
		case strings.Contains(tagLower, "refactor"):
			return TaskTypeRefactor
		case strings.Contains(tagLower, "docs"):
			return TaskTypeDocumentation
		case strings.Contains(tagLower, "test"):
			return TaskTypeTest
		}
	}

	// Check task name
	switch {
	case strings.Contains(nameLower, "fix") || strings.Contains(nameLower, "bug"):
		return TaskTypeBugFix
	case strings.Contains(nameLower, "add") || strings.Contains(nameLower, "implement") || strings.Contains(nameLower, "feature"):
		return TaskTypeFeature
	case strings.Contains(nameLower, "refactor") || strings.Contains(nameLower, "cleanup"):
		return TaskTypeRefactor
	case strings.Contains(nameLower, "document") || strings.Contains(nameLower, "readme"):
		return TaskTypeDocumentation
	case strings.Contains(nameLower, "test"):
		return TaskTypeTest
	default:
		return TaskTypeUnknown
	}
}

func extractRequirements(description string) []string {
	requirements := []string{}

	// Look for common requirement patterns
	patterns := []string{
		`(?i)requirements?:\s*\n((?:[-*]\s*.+\n?)+)`,
		`(?i)todo:\s*\n((?:[-*]\s*.+\n?)+)`,
		`(?i)tasks?:\s*\n((?:[-*]\s*.+\n?)+)`,
	}

	for _, pattern := range patterns {
		re := regexp.MustCompile(pattern)
		matches := re.FindStringSubmatch(description)
		if len(matches) > 1 {
			items := extractBulletPoints(matches[1])
			requirements = append(requirements, items...)
		}
	}

	// If no structured requirements found, use numbered or bulleted lists
	if len(requirements) == 0 {
		requirements = extractBulletPoints(description)
	}

	return requirements
}

func extractAcceptanceCriteria(description string) []string {
	criteria := []string{}

	patterns := []string{
		`(?i)acceptance criteria:\s*\n((?:[-*]\s*.+\n?)+)`,
		`(?i)done when:\s*\n((?:[-*]\s*.+\n?)+)`,
	}

	for _, pattern := range patterns {
		re := regexp.MustCompile(pattern)
		matches := re.FindStringSubmatch(description)
		if len(matches) > 1 {
			items := extractBulletPoints(matches[1])
			criteria = append(criteria, items...)
		}
	}

	return criteria
}

func extractBulletPoints(text string) []string {
	items := []string{}
	re := regexp.MustCompile(`(?m)^\s*[-*•]\s*(.+)$`)
	matches := re.FindAllStringSubmatch(text, -1)

	for _, match := range matches {
		if len(match) > 1 {
			item := strings.TrimSpace(match[1])
			if item != "" {
				items = append(items, item)
			}
		}
	}

	return items
}

func extractFilePaths(description string) []string {
	paths := []string{}

	// Match common file path patterns
	re := regexp.MustCompile(`(?:^|\s)([\w/.-]+\.\w+)`)
	matches := re.FindAllStringSubmatch(description, -1)

	for _, match := range matches {
		if len(match) > 1 {
			paths = append(paths, match[1])
		}
	}

	return paths
}

func checkTestsRequired(description string, tags []clickup.Tag) bool {
	descLower := strings.ToLower(description)

	// Check description for test mentions
	if strings.Contains(descLower, "test") ||
	   strings.Contains(descLower, "coverage") ||
	   strings.Contains(descLower, "unit test") {
		return true
	}

	// Check tags
	for _, tag := range tags {
		if strings.Contains(strings.ToLower(tag.Name), "test") {
			return true
		}
	}

	return false
}
