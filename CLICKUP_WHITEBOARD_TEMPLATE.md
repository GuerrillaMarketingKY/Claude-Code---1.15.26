# ClickUp Dashboard Whiteboard - Claude Automation Schema

## 📋 To Create After Testing

After a few successful 15-minute cycles, we'll create a visual whiteboard in your ClickUp Dashboard showing how the automation works.

---

## 🎨 Whiteboard Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│         🤖 CLAUDE AUTOMATION - HOW IT WORKS                    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  📅 SCHEDULE                                          │     │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │     │
│  │  9:44 AM - 5:00 PM CST                               │     │
│  │  15 min ON / 15 min OFF                              │     │
│  │  Monday - Friday                                      │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  🔍 WHAT I MONITOR                                    │     │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │     │
│  │                                                       │     │
│  │  ⏰ Deadlines                                         │     │
│  │     └─ Warns 2 days before due date                  │     │
│  │     └─ Posts urgent reminders                        │     │
│  │     └─ Tags all assignees                            │     │
│  │                                                       │     │
│  │  💤 Stale Tasks                                       │     │
│  │     └─ No updates in 24+ hours                       │     │
│  │     └─ Posts gentle reminders                        │     │
│  │     └─ Keeps tasks moving                            │     │
│  │                                                       │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  🔄 WORKFLOW                                          │     │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │     │
│  │                                                       │     │
│  │  1. Scan entire workspace                            │     │
│  │     └─ All spaces, folders, lists                    │     │
│  │                                                       │     │
│  │  2. Analyze each task                                │     │
│  │     └─ Check deadline proximity                      │     │
│  │     └─ Check last update time                        │     │
│  │                                                       │     │
│  │  3. Post reminders                                   │     │
│  │     └─ Add comment to task                           │     │
│  │     └─ Tag assignees                                 │     │
│  │     └─ Include context                               │     │
│  │                                                       │     │
│  │  4. Wait 5 minutes                                   │     │
│  │     └─ Repeat within cycle                           │     │
│  │                                                       │     │
│  │  5. Take 15 min break                                │     │
│  │     └─ Then start next cycle                         │     │
│  │                                                       │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  💬 WHAT MY COMMENTS LOOK LIKE                        │     │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │     │
│  │                                                       │     │
│  │  Deadline Warning:                                   │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │ ⚠️ URGENT: Deadline Approaching!           │     │     │
│  │  │                                            │     │     │
│  │  │ @john @sarah                               │     │     │
│  │  │                                            │     │     │
│  │  │ This task is due in 8 hours               │     │     │
│  │  │ (2026-01-17 14:00).                       │     │     │
│  │  │                                            │     │     │
│  │  │ Please update status or adjust deadline.  │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  │                                                       │     │
│  │  Stale Task Warning:                                 │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │ 🔔 Task Update Reminder                    │     │     │
│  │  │                                            │     │     │
│  │  │ @mike                                      │     │     │
│  │  │                                            │     │     │
│  │  │ This task hasn't been updated in 3 days   │     │     │
│  │  │ (last update: 2026-01-14 10:30).          │     │     │
│  │  │                                            │     │     │
│  │  │ Please provide a status update.           │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  │                                                       │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  📊 TODAY'S STATS                                     │     │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │     │
│  │                                                       │     │
│  │  Tasks Monitored:    [NUMBER]                        │     │
│  │  Deadline Warnings:  [NUMBER]                        │     │
│  │  Stale Reminders:    [NUMBER]                        │     │
│  │  Cycles Run:         [NUMBER]                        │     │
│  │  Last Check:         [TIME]                          │     │
│  │                                                       │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  🎯 BENEFITS                                          │     │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │     │
│  │                                                       │     │
│  │  ✅ Never miss a deadline                            │     │
│  │  ✅ Keep all tasks moving forward                    │     │
│  │  ✅ Automatic reminders (no manual checking)         │     │
│  │  ✅ Team stays informed                              │     │
│  │  ✅ Reduces task management overhead                 │     │
│  │                                                       │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  ⚙️ SETTINGS (Can Be Adjusted)                       │     │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │     │
│  │                                                       │     │
│  │  Work Hours:    9:44 AM - 5:00 PM                   │     │
│  │  Cycle Length:  15 minutes on                        │     │
│  │  Break Length:  15 minutes off                       │     │
│  │  Deadline Warn: 2 days before                        │     │
│  │  Stale After:   24 hours                             │     │
│  │                                                       │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  🆘 IF YOU NEED HELP                                  │     │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │     │
│  │                                                       │     │
│  │  • False alarm? Let us know                          │     │
│  │  • Want different timing? We can adjust              │     │
│  │  • Not getting reminders? Check your task settings   │     │
│  │  • Questions? Contact [ADMIN NAME]                   │     │
│  │                                                       │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│         Last Updated: [DATE]                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 How to Create in ClickUp

After successful testing:

1. **Go to ClickUp Dashboard**
2. **Click "Add Widget" → "Whiteboard"**
3. **Create new whiteboard: "Claude Automation Schema"**
4. **Use shapes, text boxes, and connectors to create the visual**
5. **Make it colorful and easy to understand**
6. **Pin it to main dashboard so everyone sees it**

---

## 🎨 Visual Elements to Include

- **Flow chart arrows** showing the process
- **Color coding:**
  - 🟢 Green for normal operations
  - 🟡 Yellow for warnings
  - 🔴 Red for urgent
- **Icons** for each step
- **Example comments** in speech bubbles
- **Real stats** updated daily

---

## 📊 We'll Update With Real Data

After today's test, we'll add:
- ✅ Actual tasks monitored count
- ✅ Real reminder examples
- ✅ Performance metrics
- ✅ Team feedback
- ✅ Tweaks made

---

## 🎯 Goal

Make it so **anyone** on the team can:
- Understand what Claude is doing
- See the value immediately
- Know what to expect
- Report issues or suggestions

---

**Will create this after we have a few successful cycles today!**
