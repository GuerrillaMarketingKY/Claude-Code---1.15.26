# ClickUp Claude - Autonomous Task Execution

🤖 **Proof of Concept**: Autonomous software development powered by Claude Code and ClickUp integration.

## 🎯 What This Does

This is a **proof-of-concept** that demonstrates how Claude Code can work autonomously with ClickUp to complete software development tasks **end-to-end** without human intervention.

### The Vision

1. You create a task in ClickUp: "Add user authentication to API"
2. This tool fetches the task automatically
3. Claude Code autonomously:
   - Reads your codebase
   - Creates a git branch
   - Implements the feature
   - Writes tests
   - Commits changes
   - Pushes to remote
   - Creates a pull request
   - Updates the ClickUp task with results
4. You review the PR and merge

**All without you writing a single line of code.**

---

## 🆚 Claude Code vs Regular Claude

### Regular Claude (Chat Interface)
- ❌ Can only **suggest** code
- ❌ You must **manually** copy/paste
- ❌ Can't read your files directly
- ❌ Can't run commands or tests
- ❌ Can't commit to git
- ❌ Each step requires human action

### Claude Code (This Tool)
- ✅ **Directly reads/writes** files
- ✅ **Executes** commands autonomously
- ✅ **Runs tests** and validates changes
- ✅ **Commits to git** with proper messages
- ✅ **Creates PRs** automatically
- ✅ **Complete end-to-end** workflows

---

## 🏗️ Architecture

```
┌─────────────┐
│  ClickUp    │  Task created/updated
│   Task      │
└──────┬──────┘
       │
       │ 1. Fetch via API
       ▼
┌─────────────────────┐
│  ClickUp Client     │  Retrieves task details
└──────┬──────────────┘
       │
       │ 2. Parse requirements
       ▼
┌─────────────────────┐
│  Task Parser        │  Extracts:
│                     │  - Task type (bug/feature/refactor)
│                     │  - Requirements
│                     │  - Acceptance criteria
│                     │  - Files to modify
│                     │  - Test requirements
└──────┬──────────────┘
       │
       │ 3. Execute autonomously
       ▼
┌─────────────────────┐
│  Autonomous         │  Claude Code powers this step:
│  Executor           │  - Creates git branch
│                     │  - Analyzes codebase
│                     │  - Plans implementation
│                     │  - Makes code changes
│                     │  - Runs tests
│                     │  - Commits & pushes
│                     │  - Creates PR
└──────┬──────────────┘
       │
       │ 4. Update with results
       ▼
┌─────────────────────┐
│  ClickUp Task       │  Status: "Review"
│  Updated            │  Comment: "PR created: [link]"
└─────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Go 1.21 or higher
- ClickUp account with API access
- Git repository

### Installation

1. **Clone this repository**

```bash
git clone https://github.com/GuerrillaMarketingKY/Claude-Code---1.15.26.git
cd Claude-Code---1.15.26
```

2. **Create a ClickUp OAuth App**

   - Go to ClickUp Settings → Apps: https://app.clickup.com/settings/apps
   - Click "Create an App"
   - Set **Redirect URL** to: `http://localhost:8089/callback`
   - Copy your **Client ID** and **Client Secret**

   See `OAUTH_SETUP.md` for detailed instructions.

3. **Configure OAuth credentials**

```bash
cp .env.example .env
# Edit .env and add your OAuth credentials
```

Or export them directly:

```bash
export CLICKUP_CLIENT_ID='your_client_id'
export CLICKUP_CLIENT_SECRET='your_client_secret'
```

4. **Build the tool**

```bash
go build -o clickup-claude ./cmd/clickup-claude
```

5. **Authenticate with ClickUp**

```bash
./clickup-claude auth
```

This opens your browser to authorize the app. Once authorized, your token is securely stored.

---

## 📖 Usage

### Execute a Task Autonomously

```bash
./clickup-claude execute <task-id>
```

**Example:**

```bash
./clickup-claude execute 86a2zw8mv
```

**What happens:**

1. ✓ Fetches task from ClickUp
2. ✓ Parses requirements and task type
3. ✓ Updates task status to "In Progress"
4. ✓ Creates git branch: `claude/task-name-86a2zw`
5. ✓ Analyzes codebase structure
6. ✓ Plans implementation strategy
7. ✓ Implements changes autonomously
8. ✓ Runs test suite
9. ✓ Commits with proper message
10. ✓ Pushes to remote
11. ✓ Creates pull request
12. ✓ Updates ClickUp task with PR link
13. ✓ Moves task to "Review" status

### Check Task Status

```bash
./clickup-claude status <task-id>
```

Shows task details including name, status, priority, and description.

---

## 📝 How to Format ClickUp Tasks

For best results, format your ClickUp tasks like this:

### Example 1: Feature Request

**Task Name:** Add JWT authentication middleware

**Description:**
```
Requirements:
- Create JWT token validation middleware
- Protect /api/users endpoints with auth
- Add error handling for invalid tokens
- Update API documentation

Acceptance Criteria:
- Unauthorized requests return 401
- Valid tokens allow access
- Tests cover all auth scenarios
```

### Example 2: Bug Fix

**Task Name:** Fix memory leak in connection pool

**Description:**
```
Issue: Application crashes after 24 hours due to unclosed connections

Requirements:
- Add proper connection cleanup in database.go
- Implement connection timeout
- Add test for connection lifecycle
```

**Tags:** Add relevant tags like `bug`, `feature`, `refactor`, `test`

---

## 🧪 Current Status: Proof of Concept

This is a **demonstration** to show the potential of autonomous Claude Code integration.

### ✅ What Works Now

- ✅ **Full OAuth 2.0 authentication** with encrypted token storage
- ✅ Fetches tasks from ClickUp API
- ✅ Parses task requirements intelligently
- ✅ Identifies task types (bug/feature/refactor)
- ✅ Simulates autonomous execution workflow
- ✅ Updates ClickUp tasks with status
- ✅ Creates structured execution plans
- ✅ Secure token management with automatic expiration handling

### 🚧 What's Simulated (Not Yet Implemented)

- Git branch creation (simulated)
- Code analysis and modification (simulated)
- Test execution (simulated)
- Git commits and push (simulated)
- PR creation (simulated)

### 🔮 Next Steps for Full Implementation

To make this **fully autonomous**, we need to:

1. **Integrate with Claude Code API**
   - Use the Anthropic SDK to invoke Claude Code
   - Pass task requirements as prompts
   - Stream execution results back

2. **Real Git Operations**
   - Actually create branches
   - Make real commits
   - Push to GitHub/GitLab

3. **Webhook Server**
   - Listen for ClickUp webhooks
   - Trigger execution automatically
   - Run as a background service

4. **Error Handling & Recovery**
   - Handle compilation errors
   - Retry failed tests
   - Request human intervention when stuck

---

## 🔧 Project Structure

```
.
├── cmd/
│   └── clickup-claude/       # Main application entry point
│       └── main.go
├── internal/
│   ├── auth/                 # OAuth 2.0 authentication
│   │   ├── oauth.go          # OAuth flow handler
│   │   └── storage.go        # Encrypted token storage
│   ├── clickup/              # ClickUp API client
│   │   └── client.go
│   ├── parser/               # Task requirement parser
│   │   └── parser.go
│   └── executor/             # Autonomous execution engine
│       └── executor.go
├── pkg/
│   └── config/               # Configuration management
│       └── config.go
├── .claude/                  # Claude Code hooks
│   ├── hooks/
│   │   └── session-start.sh
│   └── settings.json
├── go.mod
├── .env.example
├── README.md
├── OAUTH_SETUP.md            # OAuth setup guide
└── DEMO.md
```

---

## 🎓 Why Claude Code Is Better

| Feature | Regular Claude | Claude Code |
|---------|---------------|-------------|
| **File Access** | No - you copy/paste | Yes - direct read/write |
| **Command Execution** | No - you type commands | Yes - runs bash, npm, go, etc. |
| **Git Operations** | No - you commit manually | Yes - commits, pushes, creates PRs |
| **Test Execution** | No - you run tests | Yes - runs and fixes failing tests |
| **Multi-file Changes** | No - one suggestion at a time | Yes - modifies multiple files in one workflow |
| **Continuous Operation** | No - waits for each response | Yes - completes entire task autonomously |
| **Codebase Understanding** | Limited - no direct access | Full - reads entire project structure |
| **Verification** | No - you verify manually | Yes - runs tests and validates changes |

---

## 🤝 Contributing

This is a proof-of-concept demonstrating autonomous ClickUp integration. To turn this into a fully functional system:

1. Integrate with Claude Code API
2. Implement real git operations
3. Add webhook server for automatic triggers
4. Add configuration for different project types
5. Implement error recovery mechanisms

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- Built with Claude Code (demonstrating its own capabilities!)
- Powered by Anthropic's Claude API
- Integrated with ClickUp's REST API

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check ClickUp API docs: https://clickup.com/api
- Claude Code docs: https://docs.anthropic.com/

---

**Built autonomously by Claude Code** 🤖✨
