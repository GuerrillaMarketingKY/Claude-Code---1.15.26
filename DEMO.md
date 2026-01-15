# 🎬 Demo Guide - ClickUp Claude Integration

This guide shows you how to test the proof-of-concept with a real ClickUp task.

## 📋 Prerequisites

You need:
1. A ClickUp account
2. Your ClickUp API token
3. Your ClickUp Team/Workspace ID
4. At least one task in your ClickUp workspace

---

## 🔑 Step 1: Get Your ClickUp Credentials

### Get API Token

1. Log into ClickUp
2. Click your profile avatar (bottom left)
3. Go to **Settings** → **Apps**
4. Under **API Token**, click **Generate**
5. Copy the token (starts with `pk_`)

### Get Team ID

**Option A: Using Browser**

1. Go to your ClickUp workspace
2. Look at the URL: `https://app.clickup.com/TEAM_ID/...`
3. The number after `app.clickup.com/` is your Team ID

**Option B: Using API**

```bash
curl -H "Authorization: YOUR_API_TOKEN" \
     https://api.clickup.com/api/v2/team
```

Look for `"id"` in the response.

---

## 🚀 Step 2: Configure & Build

1. **Set environment variables:**

```bash
export CLICKUP_API_TOKEN='pk_your_token_here'
export CLICKUP_TEAM_ID='your_team_id_here'
```

2. **Build the tool (if not already built):**

```bash
go build -o clickup-claude ./cmd/clickup-claude
```

---

## 📝 Step 3: Create a Test Task in ClickUp

Create a new task with structured requirements. Here's an example:

**Task Name:** Test Claude Code Integration

**Description:**
```
Requirements:
- Create a simple "Hello World" function
- Add unit test for the function
- Add documentation comments

Acceptance Criteria:
- Function returns "Hello, World!"
- Test passes successfully
- Code is well documented
```

**Tags:** `feature`, `test`

**Copy the Task ID** from the URL:
`https://app.clickup.com/t/TASK_ID` ← Copy this part

---

## 🎯 Step 4: Run the Demo

### Check Task Status

First, verify you can fetch the task:

```bash
./clickup-claude status YOUR_TASK_ID
```

You should see the task details displayed.

### Execute Autonomously (Simulated)

Now run the autonomous execution:

```bash
./clickup-claude execute YOUR_TASK_ID
```

**What you'll see:**

```
🚀 ClickUp Claude - Autonomous Task Execution
============================================

📥 Fetching task YOUR_TASK_ID from ClickUp...
✓ Task fetched: Test Claude Code Integration

┌─────────────────────────────────────────────────┐
│ Task: Test Claude Code Integration             │
├─────────────────────────────────────────────────┤
│ ID:       YOUR_TASK_ID                          │
│ Status:   To Do                                 │
│ Priority: Normal                                │
└─────────────────────────────────────────────────┘

🔍 Parsing task requirements...
✓ Task type identified: feature
✓ Requirements extracted: 3
✓ Tests required: true

🤖 Beginning autonomous execution...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Starting autonomous execution for task: Test Claude Code Integration
🌿 Creating branch: claude/test-claude-code-integration-abc123
🔍 Analyzing codebase structure...
   Task type: feature
   Requirements found: 3
     1. Create a simple "Hello World" function
     2. Add unit test for the function
     3. Add documentation comments

📝 Creating implementation plan...
   1. Design the feature implementation
   2. Create or modify necessary files
   3. Implement core functionality
   4. Add comprehensive tests
   5. Update documentation if needed

⚙️  Implementing changes...
   ✓ Design the feature implementation
   ✓ Create or modify necessary files
   ✓ Implement core functionality
   ✓ Add comprehensive tests
   ✓ Update documentation if needed

🧪 Running test suite...
   ✓ All tests passed

💾 Committing changes...
   Commit message: feat: Test Claude Code Integration

📤 Pushing to remote: claude/test-claude-code-integration-abc123

🔀 Creating pull request...
   PR created: https://github.com/example/repo/pull/123

✅ Updating ClickUp task...

✨ Autonomous execution complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Execution Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status:           ✅ Success
Branch Created:   claude/test-claude-code-integration-abc123
Files Modified:   5
Tests Passed:     true
Commit Hash:      abc123def456
Pull Request:     https://github.com/example/repo/pull/123
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ Task completed successfully!
   The ClickUp task has been updated with the results.
```

---

## ✅ Step 5: Verify in ClickUp

Go back to your ClickUp task and check:

1. **Status changed** from "To Do" to "In Progress" and then "Review"
2. **Comment added** by the automation with execution details
3. **Task includes** branch name and PR link (simulated)

---

## 🎓 Understanding What Happened

### Current State (Proof of Concept)

This demo shows a **simulated** autonomous workflow. The tool:

- ✅ **Actually fetches** the real task from ClickUp
- ✅ **Actually parses** the task requirements intelligently
- ✅ **Actually updates** the ClickUp task status and comments
- 🎭 **Simulates** the code implementation steps

### Next Level (Full Implementation)

To make it **truly autonomous**, we would integrate with Claude Code's API to:

- Create real git branches
- Analyze actual codebase files
- Write actual code changes
- Run real tests
- Make real git commits
- Push to real remote repos
- Create real pull requests

---

## 🔧 Troubleshooting

### Error: "CLICKUP_API_TOKEN environment variable is required"

Make sure you exported the environment variables:

```bash
export CLICKUP_API_TOKEN='pk_your_token_here'
export CLICKUP_TEAM_ID='your_team_id_here'
```

### Error: "API returned status 401"

Your API token is invalid or expired. Generate a new one in ClickUp settings.

### Error: "API returned status 404"

The task ID doesn't exist or you don't have access. Double-check the task ID.

### Error: "failed to fetch task"

Check your internet connection and ClickUp API status.

---

## 📚 Next Steps

1. **Try different task types:**
   - Bug fix task
   - Refactoring task
   - Documentation task

2. **Experiment with different formats:**
   - Numbered lists vs bullet points
   - Different section headers
   - Various task tags

3. **Check the code:**
   - Look at `/internal/parser/parser.go` to see how tasks are parsed
   - Check `/internal/executor/executor.go` to see the execution workflow
   - Explore `/internal/clickup/client.go` to understand the API integration

---

## 🚀 Want More?

To turn this into a **fully functional system**, consider:

1. **Webhook integration** - Auto-trigger on task creation
2. **Real git operations** - Actually create branches and commits
3. **Claude Code API** - Use the real Anthropic API for code generation
4. **Multi-language support** - Handle Python, TypeScript, Rust, etc.
5. **Error recovery** - Handle build failures and test errors

---

**Happy testing!** 🎉
