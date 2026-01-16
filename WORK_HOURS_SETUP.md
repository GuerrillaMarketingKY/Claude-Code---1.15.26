# ClickUp Monitor - Work Hours Schedule

## 📅 Today's Test Schedule (1/16/25)

**Time:** 9:44 AM - 5:00 PM CST
**Pattern:** 15 minutes ON / 15 minutes OFF
**Purpose:** Testing and tweaking performance

---

## 🚀 Quick Start

### On Your Windows Work PC:

1. **Pull the latest code:**
```powershell
cd "D:\Projects\Claude-Code---1.15.26"
git pull
```

2. **Make sure `.env` exists with your credentials:**
```env
CLICKUP_API_TOKEN=pk_106141823_INXP08ZZWGBDSQHJK9ZZB84IR7MOKUFS
WORKSPACE_ID=your_workspace_id_here
```

3. **Double-click to start:**
```
start_work_monitor.bat
```

Or run manually:
```powershell
python src\clickup_monitor_scheduled.py
```

---

## 🎯 What It Does

### During Each 15-Minute Cycle:

1. **Fetches all tasks** from your workspace
2. **Checks every 5 minutes** within the cycle
3. **Finds deadline warnings** (tasks due within 2 days)
4. **Finds stale tasks** (no updates in 24+ hours)
5. **Posts comments** tagging assignees

### Then Takes a 15-Minute Break

The cycle repeats automatically until 5:00 PM.

---

## 📊 Example Output

```
======================================================================
🔄 Cycle #1 - 09:44:23 AM
   Time until 5 PM: 436 minutes
======================================================================

🔍 Check at 09:44 AM
📥 Fetching tasks from workspace...
  📁 Engineering Team
    📋 Sprint Tasks (12 tasks)
    📋 Bug Fixes (5 tasks)
✓ Total: 17 tasks

📊 Results: 1 deadline, 2 stale

⏰ Deadline Warnings:
⏰ Fix authentication bug (due in 8 hours)
   ✓ Reminder sent

💤 Stale Tasks:
💤 Update API documentation (3d stale)
   ✓ Reminder sent
💤 Review pull request #47 (2d stale)
   ✓ Reminder sent

⏸️  Waiting 5 min until next check...

🔍 Check at 09:49 AM
...

☕ Break time! Next cycle at 09:59 AM
======================================================================
```

---

## ⚙️ Adjusting the Schedule

Edit `src/clickup_monitor_scheduled.py`:

```python
# Change start time
WORK_START_HOUR = 9
WORK_START_MINUTE = 44

# Change end time
WORK_END_HOUR = 17  # 5 PM
WORK_END_MINUTE = 0

# Change cycle duration
CHECK_DURATION_MINUTES = 15  # How long to monitor
BREAK_DURATION_MINUTES = 15  # How long to rest
```

---

## 🛑 Stopping the Monitor

- Press `Ctrl+C` in the terminal window
- Or just close the window

The monitor will automatically stop at 5:00 PM.

---

## 📝 Tonight's Review Checklist

After the test day, consider adjusting:

- [ ] Check how many reminders were sent
- [ ] Review if 15 min cycles are too frequent/slow
- [ ] Adjust deadline warning threshold (currently 2 days)
- [ ] Adjust stale task threshold (currently 24 hours)
- [ ] Decide on permanent schedule
- [ ] Consider different schedules for different days

---

## 🔧 Troubleshooting

### "Outside work hours"
- Check your system time
- Script uses your local time as CST
- Adjust WORK_START_HOUR/MINUTE if needed

### "Missing credentials"
- Make sure `.env` file exists
- Check CLICKUP_API_TOKEN and WORKSPACE_ID are set

### Script stops unexpectedly
- Check internet connection
- Verify API token is still valid
- Check ClickUp API status

---

## 📈 Performance Tracking

Track these metrics today:

- Total tasks monitored: ___
- Deadline warnings sent: ___
- Stale task warnings sent: ___
- False positives: ___
- Missed tasks: ___
- System resource usage: OK / High
- Network usage: OK / High

Notes:
```
_______________________________________________
_______________________________________________
_______________________________________________
```

---

**After today, we'll adjust the schedule based on your feedback!**
