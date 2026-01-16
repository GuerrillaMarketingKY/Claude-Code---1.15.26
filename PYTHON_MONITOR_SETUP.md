# ClickUp Task Monitor - Python Edition

🤖 Autonomous monitoring system that watches your ClickUp workspace 24/7 for:
- **Approaching deadlines** (within 2 days)
- **Stale tasks** (no updates in 24+ hours)
- Automatically posts reminder comments tagging assignees

---

## 🚀 Quick Start (Windows)

### Step 1: Install Python Dependencies

```powershell
# Navigate to the project
cd "D:\Projects\Claude-Code---1.15.26"

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

1. **Copy the env template:**
```powershell
copy .env.python .env
```

2. **Edit `.env` file** and add your credentials:
```env
CLICKUP_API_TOKEN=pk_106141823_INXP08ZZWGBDSQHJK9ZZB84IR7MOKUFS
WORKSPACE_ID=your_workspace_id_here
```

**How to get your Workspace ID:**
- Go to ClickUp
- Click on your workspace name
- Look at the URL: `https://app.clickup.com/WORKSPACE_ID/...`
- Copy the number after `app.clickup.com/`

### Step 3: Test the Monitor

**Run once to test:**
```powershell
python src\clickup_monitor.py --once
```

You should see:
```
📥 Fetching all tasks from workspace...
  📁 Team: Your Team Name
    📂 Space: Space Name
      📋 List: List Name (5 tasks)

✓ Total tasks found: 25

📊 Monitoring Results:
   Deadline warnings: 2
   Stale task warnings: 3
```

---

## 🔧 Running Modes

### Mode 1: Single Check (Testing)

Run once and exit:
```powershell
python src\clickup_monitor.py --once
```

Perfect for testing or running on a schedule (cron/Task Scheduler).

### Mode 2: Continuous Monitoring

Runs forever, checking every hour:
```powershell
python src\clickup_monitor.py
```

Press `Ctrl+C` to stop.

---

## ⚙️ Configuration Options

Edit these constants in `src/clickup_monitor.py`:

```python
CHECK_INTERVAL_MINUTES = 60  # How often to check (default: 60 min)
DEADLINE_WARNING_DAYS = 2    # Warn X days before deadline
STALE_TASK_HOURS = 24       # Consider task stale after X hours
```

---

## 🤖 Running 24/7

### Option 1: Windows Task Scheduler (Recommended)

1. **Open Task Scheduler**
2. **Create Basic Task**
   - Name: `ClickUp Monitor`
   - Trigger: `When I log on` or `Daily at specific time`
   - Action: `Start a program`
   - Program: `python`
   - Arguments: `D:\Projects\Claude-Code---1.15.26\src\clickup_monitor.py`
   - Start in: `D:\Projects\Claude-Code---1.15.26`

3. **Set to repeat every hour:**
   - Go to task properties → Triggers
   - Edit trigger → Advanced settings
   - Check "Repeat task every: 1 hour"
   - Duration: Indefinitely

### Option 2: Run as Background Process

```powershell
# Start in background (PowerShell)
Start-Process python -ArgumentList "src\clickup_monitor.py" -WindowStyle Hidden

# Or use Windows Service wrapper:
# Install NSSM (Non-Sucking Service Manager)
nssm install ClickUpMonitor "C:\Python39\python.exe" "D:\Projects\Claude-Code---1.15.26\src\clickup_monitor.py"
```

### Option 3: Cloud Hosting (Best for 24/7)

Deploy to a cloud service that runs continuously:

**Heroku:**
```bash
# Create Procfile
echo "worker: python src/clickup_monitor.py" > Procfile

# Deploy
heroku create clickup-monitor
git push heroku main
heroku ps:scale worker=1
```

**AWS EC2, Google Cloud, or DigitalOcean:**
Run the script on a small VM instance ($5-10/month).

---

## 📋 What It Does

### Deadline Warnings

When a task's deadline is within 2 days, it posts:

```
⚠️ URGENT: Deadline Approaching!

@username1 @username2

This task is due in **6 hours** (2026-01-17 14:00).

Please update the status or adjust the deadline if needed.
```

### Stale Task Warnings

When a task hasn't been updated in 24+ hours, it posts:

```
🔔 Task Update Reminder

@username1 @username2

This task hasn't been updated in **3 days** (last update: 2026-01-14 10:30).

Please provide a status update or move the task forward.
```

### Smart Reminders

- ✅ Won't spam - only sends one reminder per task per day
- ✅ Tags all assignees automatically
- ✅ Adjusts urgency based on time remaining
- ✅ Tracks processed reminders to avoid duplicates

---

## 🧪 Testing

### Test with one task:

```powershell
# Run once and check output
python src\clickup_monitor.py --once
```

### Verify it found your tasks:

Look for output like:
```
📥 Fetching all tasks from workspace...
  📁 Team: Marketing Team
    📂 Space: Q1 2026 Projects
      📋 List: Active Tasks (12 tasks)
      📋 List: Backlog (8 tasks)

✓ Total tasks found: 20
```

### Check ClickUp:

After running, go to ClickUp and check tasks - you should see comments posted by your account.

---

## 🛠️ Troubleshooting

### "CLICKUP_API_TOKEN not found"

**Fix:** Make sure `.env` file exists and has your token:
```powershell
type .env
```

### "Error fetching teams: 401"

**Fix:** Your API token is invalid. Get a new one from ClickUp Settings → Apps.

### "No tasks found"

**Fix:** Check your WORKSPACE_ID is correct. Try getting it from the URL when you're in ClickUp.

### Script crashes or errors

**Fix:** Check Python version (need 3.7+):
```powershell
python --version
```

---

## 📊 Example Output

```
==============================================================
🔍 Starting monitoring check at 2026-01-16 15:30:00
==============================================================

📥 Fetching all tasks from workspace...
  📁 Team: Engineering
    📂 Space: Product Development
      📋 List: Sprint 5 (15 tasks)
      📋 List: Bugs (7 tasks)

✓ Total tasks found: 22

📊 Monitoring Results:
   Deadline warnings: 2
   Stale task warnings: 3

⏰ Deadline Warnings:

⚠️ URGENT: Fix login authentication bug (due in 8 hours)
   ✓ Reminder sent to task 86aeg64f4

📅 Reminder: Update user dashboard UI (due in 1 day)
   ✓ Reminder sent to task 93hdk27s9

💤 Stale Task Warnings:

💤 Stale: Implement payment gateway (3 days since update)
   ✓ Reminder sent to task 72ksl39dk

💤 Stale: Database migration (2 days since update)
   ✓ Reminder sent to task 61msk28fj

⏸️  Waiting until next check at 16:30:00...
==============================================================
```

---

## 🎯 Next Steps

1. **Test it first** with `--once` mode
2. **Adjust settings** in the code if needed
3. **Set up Task Scheduler** for automated runs
4. **Or deploy to cloud** for true 24/7 monitoring

---

## 🔗 Integration with Go Tool

This Python monitor is **separate from** the Go-based autonomous executor. Use them together:

- **Python Monitor:** Watches for deadlines and inactivity
- **Go Executor:** Executes tasks autonomously when assigned to Claude

Both can run simultaneously!

---

**Questions?** Check the main README.md or open an issue on GitHub.
