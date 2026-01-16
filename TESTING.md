# Testing Guide

## ⚠️ Important Note

This code was developed in a sandboxed environment without external internet access. **You need to test it on your local machine** where it can reach api.clickup.com.

---

## 🚀 Quick Test (On Your Local Machine)

### Step 1: Build the Binary

```bash
go build -o clickup-claude ./cmd/clickup-claude
```

### Step 2: Set Your Access Token

```bash
export CLICKUP_ACCESS_TOKEN='pk_106141823_INXP08ZZWGBDSQHJK9ZZB84IR7MOKUFS'
```

### Step 3: Test Task Status

```bash
./clickup-claude status 86aeg64f4
```

**Expected output:**
```
📥 Fetching task 86aeg64f4...

┌─────────────────────────────────────────────────┐
│ Task: Your Task Name                            │
├─────────────────────────────────────────────────┤
│ ID:       86aeg64f4                              │
│ Status:   To Do                                  │
│ Priority: Normal                                 │
│ URL:      https://app.clickup.com/t/86aeg64f4   │
└─────────────────────────────────────────────────┘
```

### Step 4: Test Autonomous Execution

```bash
./clickup-claude execute 86aeg64f4
```

This will:
- ✅ Fetch the task
- ✅ Parse requirements
- ✅ Simulate autonomous execution
- ✅ Update task status in ClickUp
- ✅ Add comments with execution results

---

## 🔧 Automated Test Script

Run the included test script:

```bash
./test-clickup.sh
```

This runs both status and execute commands automatically.

---

## 🐛 Troubleshooting

### Error: "Could not resolve host: api.clickup.com"

**Cause:** No internet access or DNS issues

**Solution:** Make sure you're on a machine with internet access

### Error: "API returned status 401"

**Cause:** Invalid or expired access token

**Solution:**
1. Go to ClickUp Settings → Apps
2. Generate a new access token
3. Update the `CLICKUP_ACCESS_TOKEN` environment variable

### Error: "API returned status 404"

**Cause:** Task ID doesn't exist or you don't have access

**Solution:**
1. Verify the task ID from the ClickUp URL
2. Make sure you have access to the task

### Error: "API returned status 403: Forbidden"

**Cause:** Token doesn't have the required permissions

**Solution:**
1. Check the token has read/write permissions for tasks
2. Verify you're using the correct workspace/team

---

## ✅ What Should Work

Once tested on a machine with internet access, you should be able to:

1. **Fetch task details** with `status` command
2. **Execute tasks autonomously** with `execute` command
3. **See task updates** in ClickUp (status changes, comments)
4. **View execution logs** in terminal

---

## 📝 Next Steps After Testing

1. Test with different task types (bug, feature, refactor)
2. Try tasks with structured requirements
3. Verify ClickUp task updates work correctly
4. Report any issues or improvements needed

---

**Note:** The autonomous execution is currently simulated. To make it fully functional, you would integrate with the Claude API to actually generate and execute code changes.
