"""
ClickUp Task Monitor - Scheduled Work Hours Edition
Runs 20 minutes on, 20 minutes off during work hours only
"""

import os
import time
import requests
from datetime import datetime, timedelta, time as dt_time
from dotenv import load_dotenv
from typing import List, Dict, Optional
import sys

# Load environment variables
load_dotenv()

CLICKUP_API_TOKEN = os.getenv('CLICKUP_API_TOKEN')
WORKSPACE_ID = os.getenv('WORKSPACE_ID')
BASE_URL = 'https://api.clickup.com/api/v2'

# Work Hours Configuration (CST) - Today's Test Schedule (1/16/25)
WORK_START_HOUR = 9
WORK_START_MINUTE = 44
WORK_END_HOUR = 17  # 5 PM in 24-hour format
WORK_END_MINUTE = 0

# Monitoring Configuration - Today's Test Schedule (15 min on/off)
CHECK_DURATION_MINUTES = 15  # Run for 15 minutes
BREAK_DURATION_MINUTES = 15  # Break for 15 minutes
DEADLINE_WARNING_DAYS = 2
STALE_TASK_HOURS = 24


class ClickUpMonitor:
    def __init__(self, api_token: str, workspace_id: str):
        self.api_token = api_token
        self.workspace_id = workspace_id
        self.headers = {
            'Authorization': api_token,
            'Content-Type': 'application/json'
        }
        self.processed_reminders = set()

    def get_all_teams(self) -> List[Dict]:
        """Get all teams in the workspace"""
        try:
            response = requests.get(
                f'{BASE_URL}/team',
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get('teams', [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching teams: {e}")
            return []

    def get_all_spaces(self, team_id: str) -> List[Dict]:
        """Get all spaces in a team"""
        try:
            response = requests.get(
                f'{BASE_URL}/team/{team_id}/space',
                headers=self.headers,
                params={'archived': 'false'}
            )
            response.raise_for_status()
            return response.json().get('spaces', [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching spaces: {e}")
            return []

    def get_all_lists(self, space_id: str) -> List[Dict]:
        """Get all lists in a space"""
        try:
            response = requests.get(
                f'{BASE_URL}/space/{space_id}/list',
                headers=self.headers,
                params={'archived': 'false'}
            )
            response.raise_for_status()
            return response.json().get('lists', [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching lists: {e}")
            return []

    def get_tasks_in_list(self, list_id: str) -> List[Dict]:
        """Get all tasks in a list"""
        try:
            response = requests.get(
                f'{BASE_URL}/list/{list_id}/task',
                headers=self.headers,
                params={
                    'archived': 'false',
                    'include_closed': 'false'
                }
            )
            response.raise_for_status()
            return response.json().get('tasks', [])
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching tasks: {e}")
            return []

    def get_all_tasks(self) -> List[Dict]:
        """Get all active tasks across the entire workspace"""
        all_tasks = []
        print("📥 Fetching tasks from workspace...")

        teams = self.get_all_teams()
        for team in teams:
            team_id = team['id']
            team_name = team['name']
            print(f"  📁 {team_name}")

            spaces = self.get_all_spaces(team_id)
            for space in spaces:
                space_id = space['id']
                space_name = space['name']

                lists = self.get_all_lists(space_id)
                for list_item in lists:
                    list_id = list_item['id']
                    list_name = list_item['name']
                    tasks = self.get_tasks_in_list(list_id)
                    all_tasks.extend(tasks)
                    if tasks:
                        print(f"    📋 {list_name} ({len(tasks)} tasks)")

        print(f"✓ Total: {len(all_tasks)} tasks\n")
        return all_tasks

    def check_approaching_deadline(self, task: Dict) -> Optional[Dict]:
        """Check if task has a deadline approaching"""
        due_date_str = task.get('due_date')
        if not due_date_str:
            return None

        due_date = datetime.fromtimestamp(int(due_date_str) / 1000)
        now = datetime.now()
        time_until_due = due_date - now

        if timedelta(0) < time_until_due <= timedelta(days=DEADLINE_WARNING_DAYS):
            hours_remaining = time_until_due.total_seconds() / 3600
            return {
                'type': 'deadline',
                'task': task,
                'hours_remaining': hours_remaining,
                'due_date': due_date
            }
        return None

    def check_stale_task(self, task: Dict) -> Optional[Dict]:
        """Check if task hasn't been updated recently"""
        date_updated_str = task.get('date_updated')
        if not date_updated_str:
            return None

        last_updated = datetime.fromtimestamp(int(date_updated_str) / 1000)
        now = datetime.now()
        hours_since_update = (now - last_updated).total_seconds() / 3600

        if hours_since_update >= STALE_TASK_HOURS:
            return {
                'type': 'stale',
                'task': task,
                'hours_since_update': hours_since_update,
                'last_updated': last_updated
            }
        return None

    def add_task_comment(self, task_id: str, comment_text: str) -> bool:
        """Add a comment to a task"""
        try:
            response = requests.post(
                f'{BASE_URL}/task/{task_id}/comment',
                headers=self.headers,
                json={'comment_text': comment_text}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding comment: {e}")
            return False

    def format_assignee_mentions(self, assignees: List[Dict]) -> str:
        """Format assignee mentions"""
        if not assignees:
            return ""
        mentions = [f"@{a.get('username', 'User')}" for a in assignees]
        return " ".join(mentions)

    def process_deadline_warning(self, alert: Dict) -> None:
        """Send deadline warning"""
        task = alert['task']
        task_id = task['id']
        task_name = task['name']
        hours_remaining = alert['hours_remaining']
        due_date = alert['due_date']

        reminder_key = f"deadline_{task_id}_{due_date.date()}"
        if reminder_key in self.processed_reminders:
            return

        assignees = task.get('assignees', [])
        mentions = self.format_assignee_mentions(assignees)

        if hours_remaining < 24:
            urgency = "⚠️ URGENT"
            time_desc = f"{int(hours_remaining)} hours"
        else:
            urgency = "📅 Reminder"
            days = int(hours_remaining / 24)
            time_desc = f"{days} day{'s' if days > 1 else ''}"

        comment = f"""{urgency}: Deadline Approaching!

{mentions}

This task is due in **{time_desc}** ({due_date.strftime('%Y-%m-%d %H:%M')}).

Please update the status or adjust the deadline if needed."""

        print(f"⏰ {task_name} (due in {time_desc})")
        if self.add_task_comment(task_id, comment):
            self.processed_reminders.add(reminder_key)
            print(f"   ✓ Reminder sent")

    def process_stale_task_warning(self, alert: Dict) -> None:
        """Send stale task warning"""
        task = alert['task']
        task_id = task['id']
        task_name = task['name']
        hours_since_update = alert['hours_since_update']
        last_updated = alert['last_updated']

        reminder_key = f"stale_{task_id}_{datetime.now().date()}"
        if reminder_key in self.processed_reminders:
            return

        assignees = task.get('assignees', [])
        mentions = self.format_assignee_mentions(assignees)
        days_since_update = int(hours_since_update / 24)

        comment = f"""🔔 Task Update Reminder

{mentions}

This task hasn't been updated in **{days_since_update} day{'s' if days_since_update > 1 else ''}** (last update: {last_updated.strftime('%Y-%m-%d %H:%M')}).

Please provide a status update or move the task forward."""

        print(f"💤 {task_name} ({days_since_update}d stale)")
        if self.add_task_comment(task_id, comment):
            self.processed_reminders.add(reminder_key)
            print(f"   ✓ Reminder sent")

    def monitor_once(self) -> Dict[str, int]:
        """Run a single monitoring check"""
        tasks = self.get_all_tasks()

        deadline_alerts = []
        stale_alerts = []

        for task in tasks:
            deadline_alert = self.check_approaching_deadline(task)
            if deadline_alert:
                deadline_alerts.append(deadline_alert)

            stale_alert = self.check_stale_task(task)
            if stale_alert:
                stale_alerts.append(stale_alert)

        print(f"📊 Results: {len(deadline_alerts)} deadline, {len(stale_alerts)} stale\n")

        if deadline_alerts:
            print("⏰ Deadline Warnings:")
            for alert in deadline_alerts:
                self.process_deadline_warning(alert)
            print()

        if stale_alerts:
            print("💤 Stale Tasks:")
            for alert in stale_alerts:
                self.process_stale_task_warning(alert)
            print()

        if not deadline_alerts and not stale_alerts:
            print("✅ All tasks on track!\n")

        return {
            'total_tasks': len(tasks),
            'deadline_warnings': len(deadline_alerts),
            'stale_warnings': len(stale_alerts)
        }


def is_within_work_hours() -> bool:
    """Check if current time is within work hours (CST)"""
    now = datetime.now()
    current_time = now.time()

    start_time = dt_time(WORK_START_HOUR, WORK_START_MINUTE)
    end_time = dt_time(WORK_END_HOUR, WORK_END_MINUTE)

    return start_time <= current_time <= end_time


def get_next_check_time() -> datetime:
    """Calculate next check time (after break)"""
    return datetime.now() + timedelta(minutes=BREAK_DURATION_MINUTES)


def get_work_end_time() -> datetime:
    """Get today's work end time"""
    now = datetime.now()
    return now.replace(hour=WORK_END_HOUR, minute=WORK_END_MINUTE, second=0, microsecond=0)


def main():
    print(f"""
{'='*70}
🕐 ClickUp Monitor - Scheduled Work Hours Mode
{'='*70}
Schedule: {WORK_START_HOUR}:{WORK_START_MINUTE:02d} - {WORK_END_HOUR}:{WORK_END_MINUTE:02d} CST
Pattern:  {CHECK_DURATION_MINUTES} min ON / {BREAK_DURATION_MINUTES} min OFF
Deadline: {DEADLINE_WARNING_DAYS} days warning
Stale:    {STALE_TASK_HOURS} hours threshold
{'='*70}
""")

    # Validate credentials
    if not CLICKUP_API_TOKEN or not WORKSPACE_ID:
        print("❌ Missing credentials in .env file")
        print("   Need: CLICKUP_API_TOKEN and WORKSPACE_ID")
        return

    # Check if we're in work hours
    if not is_within_work_hours():
        now = datetime.now()
        print(f"⏸️  Outside work hours ({now.strftime('%I:%M %p')})")
        print(f"   Work hours: {WORK_START_HOUR}:{WORK_START_MINUTE:02d} AM - {WORK_END_HOUR}:{WORK_END_MINUTE:02d} PM CST")
        return

    monitor = ClickUpMonitor(CLICKUP_API_TOKEN, WORKSPACE_ID)

    try:
        cycle_num = 1
        while is_within_work_hours():
            work_end = get_work_end_time()
            time_until_end = work_end - datetime.now()

            print(f"\n{'='*70}")
            print(f"🔄 Cycle #{cycle_num} - {datetime.now().strftime('%I:%M:%S %p')}")
            print(f"   Time until 5 PM: {int(time_until_end.total_seconds() / 60)} minutes")
            print(f"{'='*70}\n")

            # Monitor for CHECK_DURATION_MINUTES
            check_end_time = datetime.now() + timedelta(minutes=CHECK_DURATION_MINUTES)

            while datetime.now() < check_end_time and is_within_work_hours():
                print(f"🔍 Check at {datetime.now().strftime('%I:%M %p')}")
                monitor.monitor_once()

                # Wait 5 minutes before next check within this cycle
                if datetime.now() < check_end_time:
                    wait_mins = min(5, (check_end_time - datetime.now()).total_seconds() / 60)
                    if wait_mins > 0:
                        print(f"⏸️  Waiting {int(wait_mins)} min until next check...")
                        time.sleep(wait_mins * 60)

            # Break time
            if is_within_work_hours():
                next_check = get_next_check_time()

                # Don't start break if we're past work hours
                if next_check > work_end:
                    print(f"\n🏁 Work day complete at {datetime.now().strftime('%I:%M %p')}")
                    break

                print(f"\n☕ Break time! Next cycle at {next_check.strftime('%I:%M %p')}")
                print(f"{'='*70}\n")

                time.sleep(BREAK_DURATION_MINUTES * 60)
                cycle_num += 1

        print(f"\n{'='*70}")
        print(f"🏁 Monitoring complete - Outside work hours")
        print(f"{'='*70}\n")

    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped by user\n")


if __name__ == '__main__':
    main()
